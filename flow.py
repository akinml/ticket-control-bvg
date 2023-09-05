from prefect import flow
from pipeline import *
from ticket_control.big_query_download_raw import *
from ticket_control.big_query_upload_raw import *
from ticket_control.big_query_download_processed import *
from ticket_control.big_query_upload_processed import *
from ticket_control.telegramm_update_prod import *
from prefect_gcp import GcpCredentials
from prefect.filesystems import GitHub
from prefect_github import GitHubCredentials
from prefect_github.repository import GitHubRepository

github_repository_block = GitHubRepository.load("github-repo2")
github_credentials_block = GitHubCredentials.load("github")
github_block = GitHub.load("github-repo")
gcp_credentials_block = GcpCredentials.load("prefect")


@flow(name="pipeline")
def update_flow():
    df = get_update()
    upload_big_query_raw(df)
    df = pipeline(df)
    upload_big_query_processed(df)


if __name__ == "__main__":
    update_flow()
