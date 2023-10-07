from fastapi.testclient import TestClient
from fastapi import status
from routes.semestre import semestre_router  # Assurez-vous d'importer correctement votre application FastAPI

client = TestClient(app=semestre_router)

def test_semestre():
    # Test de la route ''
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste de dictionnaires

    # # Test de la route '/{id}'
    # response = client.get('/2')  # Remplacez 2 par l'ID que vous souhaitez tester
    # assert response.status_code == status.HTTP_200_OK
    # assert isinstance(response.json(), dict)  # Vérifie que la réponse est un dictionnaire

    # Test de la création d'un nouveau semestre
    new_semestre = {
            "nom": "sem add",
            "id_fil": 17,
            "date_debut": "2023-10-05T20:50:37.038Z",
            "date_fin": "2023-10-05T20:50:37.038Z"
            }
    response = client.post('/', json=new_semestre)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0 

    # Test de la mise à jour d'un semestre
    updated_semestre = {
            "nom": "sem mod",
            "id_fil": 17,
            "date_debut": "2023-10-05T20:50:37.038Z",
            "date_fin": "2023-10-05T20:50:37.038Z"
            }
    response = client.put('/2', json=updated_semestre)  # Remplacez 7 par l'ID du semestre à mettre à jour
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0 

    # Test de la suppression d'un semestre
    response = client.delete('/2')  # Remplacez 7 par l'ID du semestre à supprimer
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0 
