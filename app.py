import os
import json
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.googleapis import AuthorizedSession
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import base64
from PIL import Image
import PyPDF2
import io

app = Flask(__name__)
CORS(app)

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'
KNOWLEDGE_BASE_FILE = 'knowledge_base.json'

# Stockage en mémoire pour la session
knowledge_base = {}
drive_service = None

# ==================== AUTHENTIFICATION GOOGLE DRIVE ====================

def authenticate_google_drive():
    """Authentifier avec Google Drive"""
    global drive_service
    
    creds = None
    
    # Charger le token existant
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Si pas de token valide, créer un nouveau
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarder le token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

# ==================== GESTION DES FICHIERS ====================

def get_folder_id(folder_name):
    """Trouver l'ID d'un dossier par son nom"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        return items[0]['id']
    return None

def list_files_in_folder(folder_id):
    """Lister tous les fichiers d'un dossier"""
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, mimeType, size)',
        pageSize=100
    ).execute()
    
    return results.get('files', [])

def download_file(file_id, file_name):
    """Télécharger un fichier depuis Google Drive"""
    request = drive_service.files().get_media(fileId=file_id)
    file_content = request.execute()
    return file_content

# ==================== EXTRACTION DE CONTENU ====================

def extract_pdf_text(pdf_content):
    """Extraire le texte d'un PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Erreur extraction PDF: {e}")
        return ""

def extract_image_text(image_content, filename):
    """Extraire le texte d'une image (optionnel - requiert OCR)"""
    try:
        image = Image.open(io.BytesIO(image_content))
        # Pour une vrai OCR, utiliseriez pytesseract ou similar
        # Pour maintenant, on retourne juste le filename
        return f"[Image: {filename}] - Contenu non analysé (OCR requis)"
    except Exception as e:
        print(f"Erreur extraction image: {e}")
        return ""

def extract_text_file(content):
    """Extraire le texte d'un fichier texte"""
    try:
        return content.decode('utf-8')
    except:
        return ""

# ==================== BASE DE CONNAISSANCE ====================

def build_knowledge_base(folder_name):
    """Construire la base de connaissance depuis les fichiers du dossier"""
    global knowledge_base
    
    folder_id = get_folder_id(folder_name)
    if not folder_id:
        return {"error": f"Dossier '{folder_name}' non trouvé"}
    
    files = list_files_in_folder(folder_id)
    knowledge_base = {
        "folder_name": folder_name,
        "documents": [],
        "indexed_at": str(__import__('datetime').datetime.now())
    }
    
    supported_types = {
        'application/pdf': '.pdf',
        'text/plain': '.txt',
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'text/markdown': '.md'
    }
    
    for file in files:
        if file['mimeType'] in supported_types:
            try:
                print(f"Traitement: {file['name']}...")
                file_content = download_file(file['id'], file['name'])
                
                # Extraire le texte selon le type
                text_content = ""
                if file['mimeType'] == 'application/pdf':
                    text_content = extract_pdf_text(file_content)
                elif file['mimeType'] == 'text/plain':
                    text_content = extract_text_file(file_content)
                elif file['mimeType'] in ['image/png', 'image/jpeg']:
                    text_content = extract_image_text(file_content, file['name'])
                elif file['mimeType'] == 'text/markdown':
                    text_content = extract_text_file(file_content)
                
                knowledge_base["documents"].append({
                    "name": file['name'],
                    "type": file['mimeType'],
                    "content": text_content[:5000],  # Limiter la taille
                    "full_size": len(text_content)
                })
                
            except Exception as e:
                print(f"Erreur traitement {file['name']}: {e}")
    
    # Sauvegarder la base
    with open(KNOWLEDGE_BASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    return knowledge_base

def search_knowledge_base(query, top_k=3):
    """Chercher les documents pertinents pour une question"""
    if not knowledge_base.get("documents"):
        return []
    
    # Recherche simple par mot-clé (peut être amélioré avec embeddings)
    query_words = query.lower().split()
    results = []
    
    for doc in knowledge_base["documents"]:
        content = doc['content'].lower()
        score = sum(1 for word in query_words if word in content)
        
        if score > 0:
            results.append({
                "name": doc['name'],
                "score": score,
                "excerpt": content[:200] + "..."
            })
    
    # Trier par score et retourner top_k
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

# ==================== ROUTES API ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentifier l'utilisateur avec Google Drive"""
    try:
        authenticate_google_drive()
        return jsonify({"status": "success", "message": "Authentifié avec Google Drive"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/knowledge/build', methods=['POST'])
def build_kb():
    """Construire la base de connaissance"""
    data = request.json
    folder_name = data.get('folder_name', 'IA-Documents')
    
    result = build_knowledge_base(folder_name)
    return jsonify(result)

@app.route('/api/knowledge/status', methods=['GET'])
def kb_status():
    """État de la base de connaissance"""
    if not knowledge_base:
        return jsonify({"status": "empty", "documents": 0})
    
    return jsonify({
        "status": "loaded",
        "folder": knowledge_base.get("folder_name"),
        "documents": len(knowledge_base.get("documents", [])),
        "indexed_at": knowledge_base.get("indexed_at")
    })

@app.route('/api/knowledge/search', methods=['POST'])
def search():
    """Chercher dans la base de connaissance"""
    data = request.json
    query = data.get('query', '')
    
    results = search_knowledge_base(query)
    return jsonify({"results": results, "count": len(results)})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint chat - intègre Ollama + connaissance Google Drive"""
    data = request.json
    user_message = data.get('message', '')
    model = data.get('model', 'mistral')
    
    # Chercher les documents pertinents
    relevant_docs = search_knowledge_base(user_message)
    
    # Construire le contexte
    context = "Documents pertinents:\n"
    for doc in relevant_docs:
        context += f"\n- {doc['name']}: {doc['excerpt']}\n"
    
    # Appeler Ollama
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': f"{context}\n\nQuestion: {user_message}",
                'stream': False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "response": result.get('response', ''),
                "relevant_docs": relevant_docs
            })
        else:
            return jsonify({"error": "Erreur Ollama"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Lister tous les documents indexés"""
    docs = knowledge_base.get("documents", [])
    return jsonify({
        "total": len(docs),
        "documents": [{"name": d['name'], "type": d['type']} for d in docs]
    })

@app.route('/health', methods=['GET'])
def health():
    """Vérifier que le serveur fonctionne"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("🚀 Serveur lancé sur http://localhost:5000")
    print("📚 Base de connaissance Google Drive + Ollama")
    app.run(debug=True, port=5000)
