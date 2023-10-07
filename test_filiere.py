from fastapi.testclient import TestClient
from fastapi import status
from routes.filiere import filiere_router  # Assurez-vous que le routeur est correctement importé

client = TestClient(app=filiere_router)

def test_filiere():
    # Test de la route '/'
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste de dictionnaires

    # Test de la route '/{id}'
    response = client.get('/12')  # Remplacez 12 par l'ID que vous souhaitez tester
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste

    # Vérifie que chaque élément dans la liste est un dictionnaire
    for item in response.json():
        assert isinstance(item, dict)  # Vérifie que la réponse est un dictionnaire

    # Test de la création d'une nouvelle filiere
    new_filiere = {"nom": "Nouvelle filiere", "description": "Nouvelle filiere description", "id_dep": 12}
    response = client.post('/', json=new_filiere)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Vérifie qu'il y a au moins un élément après l'ajout

    # Test de la mise à jour d'une filiere
    updated_filiere = {"nom": "filiereModifiée", "description": "Nouvelle filiere description Modifiée", "id_dep": 12}
    response = client.put('/20', json=updated_filiere)  # Remplacez 20 par l'ID de la filiere que vous voulez mettre à jour
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

    # Test de la suppression d'une filiere
    response = client.delete('/20')  # Remplacez 20 par l'ID de la filiere que vous voulez supprimer
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
