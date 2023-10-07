from fastapi.testclient import TestClient
from fastapi import status
from routes.salle import salle_router  # Assurez-vous que le routeur est correctement importé

client = TestClient(app=salle_router)

def test_salle():
    # Test de la route '/'
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste de dictionnaires

    # Test de la route '/{id}'
    response = client.get('/2')  # Remplacez 1 par l'ID que vous souhaitez tester
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1  # Vérifie qu'il y a un seul élément dans la liste

    # Test de la création d'une nouvelle salle
    new_salle = {"nom": "Nouvelle Salle"}
    response = client.post('/', json=new_salle)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Vérifie qu'il y a au moins un élément après l'ajout

    # Test de la mise à jour d'une salle
    updated_salle = {"nom": "Salle Modifiée"}
    response = client.put('/7', json=updated_salle)  # Remplacez 1 par l'ID de la salle que vous voulez mettre à jour
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

    # Test de la suppression d'une salle
    response = client.delete('/7')  # Remplacez 1 par l'ID de la salle que vous voulez supprimer
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
