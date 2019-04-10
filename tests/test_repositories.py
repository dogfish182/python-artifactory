import pytest
import requests
import responses

from pyartifactory import ArtfictoryRepository
from pyartifactory.exception import (
    RepositoryAlreadyExistsException,
    RepositoryNotFoundException,
)
from pyartifactory.models.Auth import AuthModel
from pyartifactory.models.Repository import (
    LocalRepository,
    VirtualRepository,
    RemoteRepository,
    LocalRepositoryResponse,
    VirtualRepositoryResponse,
    RemoteRepositoryResponse,
    SimpleRepository,
)

URL = "http://localhost:8080/artifactory"
AUTH = ("user", "password_or_apiKey")

SIMPLE_REPOSITORY = SimpleRepository(
    key="test_repository", type="local", url="some-url", packageType="docker"
)
LOCAL_REPOSITORY = LocalRepository(key="test_local_repository")
LOCAL_REPOSITORY_RESPONSE = LocalRepositoryResponse(key="test_local_repository")
VIRTUAL_REPOSITORY = VirtualRepository(key="test_virtual_repository", rclass="virtual")
VIRTUAL_REPOSITORY_RESPONSE = VirtualRepositoryResponse(
    key="test_virtual_repository", rclass="virtual"
)
REMOTE_REPOSITORY = RemoteRepository(
    key="test_remote_repository", url="http://test-url.com", rclass="remote"
)
REMOTE_REPOSITORY_RESPONSE = RemoteRepositoryResponse(
    key="test_remote_repository", url="http://test-url.com", rclass="remote"
)


class TestRepositories:
    @responses.activate
    def test_create_local_repository_fail_if_user_already_exists(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_local_repo")
        with pytest.raises(RepositoryAlreadyExistsException):
            artifactory_repo.create_local_repo(LOCAL_REPOSITORY)

            artifactory_repo.get_local_repo.assert_called_once_with(
                LOCAL_REPOSITORY.key
            )

    @responses.activate
    def test_create_virtual_repository_fail_if_user_already_exists(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_virtual_repo")
        with pytest.raises(RepositoryAlreadyExistsException):
            artifactory_repo.create_virtual_repo(VIRTUAL_REPOSITORY)

            artifactory_repo.get_virtual_repo.assert_called_once_with(
                VIRTUAL_REPOSITORY.key
            )

    @responses.activate
    def test_create_remote_repository_fail_if_user_already_exists(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_remote_repo")
        with pytest.raises(RepositoryAlreadyExistsException):
            artifactory_repo.create_remote_repo(REMOTE_REPOSITORY)

            artifactory_repo.get_remote_repo.assert_called_once_with(
                REMOTE_REPOSITORY.key
            )

    @responses.activate
    def test_create_local_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=404,
        )
        responses.add(
            responses.PUT,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=201,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_local_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.create_local_repo(LOCAL_REPOSITORY)

            artifactory_repo.get_local_repo.assert_called_with(LOCAL_REPOSITORY.key)
        assert artifactory_repo.get_local_repo.call_count == 2

    @responses.activate
    def test_create_virtual_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=404,
        )
        responses.add(
            responses.PUT,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=201,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_virtual_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.create_virtual_repo(VIRTUAL_REPOSITORY)

            artifactory_repo.get_virtual_repo.assert_called_with(LOCAL_REPOSITORY.key)
        assert artifactory_repo.get_virtual_repo.call_count == 2

    @responses.activate
    def test_create_remote_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=404,
        )
        responses.add(
            responses.PUT,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=201,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_remote_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.create_remote_repo(REMOTE_REPOSITORY)

            artifactory_repo.get_remote_repo.assert_called_with(REMOTE_REPOSITORY.key)
        assert artifactory_repo.get_remote_repo.call_count == 2

    @responses.activate
    def test_get_local_repository_error_not_found(self):
        responses.add(
            responses.GET, f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}", status=404
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.get_local_repo(LOCAL_REPOSITORY.key)

    @responses.activate
    def test_get_virtual_repository_error_not_found(self):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            status=404,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.get_virtual_repo(VIRTUAL_REPOSITORY.key)

    @responses.activate
    def test_get_remote_repository_error_not_found(self):
        responses.add(
            responses.GET, f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}", status=404
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.get_remote_repo(REMOTE_REPOSITORY.key)

    @responses.activate
    def test_get_local_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_local_repo")
        artifactory_repo.get_local_repo(LOCAL_REPOSITORY.key)

        artifactory_repo.get_local_repo.assert_called_once()

    @responses.activate
    def test_get_virtual_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_virtual_repo")
        artifactory_repo.get_virtual_repo(VIRTUAL_REPOSITORY.key)

        artifactory_repo.get_virtual_repo.assert_called_once()

    @responses.activate
    def test_get_remote_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_remote_repo")
        artifactory_repo.get_remote_repo(REMOTE_REPOSITORY.key)

        artifactory_repo.get_remote_repo.assert_called_once()

    @responses.activate
    def test_list_repositories_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories",
            json=[SIMPLE_REPOSITORY.dict()],
            status=200,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "list")
        artifactory_repo.list()

        artifactory_repo.list.assert_called_once()

    @responses.activate
    def test_update_local_repository_fail_if_repo_not_found(self, mocker):
        responses.add(
            responses.GET, f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}", status=404
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_local_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.update_local_repo(LOCAL_REPOSITORY)

            artifactory_repo.get_local_repo.assert_called_once_with(
                LOCAL_REPOSITORY.key
            )

    @responses.activate
    def test_update_virtual_repository_fail_if_repo_not_found(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            status=404,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_virtual_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.update_virtual_repo(VIRTUAL_REPOSITORY)

            artifactory_repo.get_virtual_repo.assert_called_once_with(
                VIRTUAL_REPOSITORY.key
            )

    @responses.activate
    def test_update_remote_repository_fail_if_repo_not_found(self, mocker):
        responses.add(
            responses.GET, f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}", status=404
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_remote_repo")
        with pytest.raises(RepositoryNotFoundException):
            artifactory_repo.update_remote_repo(REMOTE_REPOSITORY)

            artifactory_repo.get_remote_repo.assert_called_once_with(
                REMOTE_REPOSITORY.key
            )

    @responses.activate
    def test_update_local_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        responses.add(
            responses.POST,
            f"{URL}/api/repositories/{LOCAL_REPOSITORY.key}",
            json=LOCAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )
        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_local_repo")
        artifactory_repo.update_local_repo(LOCAL_REPOSITORY)

        artifactory_repo.get_local_repo.assert_called_with(LOCAL_REPOSITORY.key)
        assert artifactory_repo.get_local_repo.call_count == 2

    @responses.activate
    def test_update_virtual_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        responses.add(
            responses.POST,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            json=VIRTUAL_REPOSITORY_RESPONSE.dict(),
            status=200,
        )
        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_virtual_repo")
        artifactory_repo.update_virtual_repo(VIRTUAL_REPOSITORY)

        artifactory_repo.get_virtual_repo.assert_called_with(VIRTUAL_REPOSITORY.key)
        assert artifactory_repo.get_virtual_repo.call_count == 2

    @responses.activate
    def test_update_remote_repository_success(self, mocker):
        responses.add(
            responses.GET,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=200,
        )

        responses.add(
            responses.POST,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            json=REMOTE_REPOSITORY_RESPONSE.dict(),
            status=200,
        )
        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        mocker.spy(artifactory_repo, "get_remote_repo")
        artifactory_repo.update_remote_repo(REMOTE_REPOSITORY)

        artifactory_repo.get_remote_repo.assert_called_with(REMOTE_REPOSITORY.key)
        assert artifactory_repo.get_remote_repo.call_count == 2

    @responses.activate
    def test_delete_repo_fail_if_repo_not_found(self, mocker):
        responses.add(
            responses.DELETE,
            f"{URL}/api/repositories/{REMOTE_REPOSITORY.key}",
            status=404,
        )

        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))

        with pytest.raises(requests.exceptions.HTTPError):
            artifactory_repo.delete(REMOTE_REPOSITORY.key)

    @responses.activate
    def test_delete_repo_success(self, mocker):
        responses.add(
            responses.DELETE,
            f"{URL}/api/repositories/{VIRTUAL_REPOSITORY.key}",
            status=204,
        )
        artifactory_repo = ArtfictoryRepository(AuthModel(url=URL, auth=AUTH))
        artifactory_repo.delete(VIRTUAL_REPOSITORY.key)