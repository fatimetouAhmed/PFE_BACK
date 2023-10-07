from fastapi.testclient import TestClient
from fastapi import status
from routes.departement import departement_router

client = TestClient(app=departement_router)

def test_departement():
    # Test de la route '/'
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

    # Test de la route '/{id}'
    response = client.get('/12')  # Testez avec un ID existant
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

    # Test de la création d'un nouveau département
    new_departement = {"nom": "Nouveau département"}
    response = client.post('/', json=new_departement)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

    # Récupérer l'ID du département créé
    # created_id = response.json()[0]["id"]

    # Test de la mise à jour du département
    updated_departement = {"nom": "Département Modifié"}
    response = client.put(f'/11', json=updated_departement)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

    # Test de la suppression du département
    response = client.delete(f'/11')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    
        # Test de la fonction read_data
    response = client.get('/nomdepartement')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

    # # Assurez-vous que les données renvoyées correspondent à ce que vous attendez
    # expected_result = [{"nom": "info"}]  # Mettez les valeurs attendues ici
    # assert response.json() == expected_result
