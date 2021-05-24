import os
import json
import requests
import sys
import semver
import github3
from jinja2 import Environment, FileSystemLoader

CONTROL_PATH = 'https://raw.githubusercontent.com/DNXLabs/docker-kube-tools/master/control.json'
LATEST_RELEASE_PATH_KUBE_TOOLS = 'https://api.github.com/repos/DNXLabs/docker-kube-tools/releases/latest'
LATEST_RELEASE_PATH_KUBECLT = 'https://dl.k8s.io/release/stable.txt'
LATEST_RELEASE_PATH_HELM = 'https://api.github.com/repos/helm/helm/releases/latest'
LATEST_RELEASE_PATH_VELERO = 'https://api.github.com/repos/vmware-tanzu/velero/releases/latest'
LATEST_RELEASE_PATH_ARGOCD = 'https://api.github.com/repos/argoproj/argo-cd/releases/latest'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY_ID = '242928140'
release_changes = False
release_message = ""
DEFAULT_BRANCH = os.getenv('DEFAULT_BRANCH', 'master')
auth_headers = {'Authorization': 'token ' + GITHUB_TOKEN}



response_control = requests.get(
    CONTROL_PATH
)

control = json.loads(response_control.text)

if response_control.status_code != 200:
    sys.exit()


def get_kube_tool_latest_version():
    response_release_kube_tools = requests.get(
        LATEST_RELEASE_PATH_KUBE_TOOLS,
        headers=auth_headers
    )

    release_kube_tools_json_obj = json.loads(response_release_kube_tools.text)
    return release_kube_tools_json_obj.get('tag_name')


def get_kubectl_latest_version():
    response_release_kubectl = requests.get(
        LATEST_RELEASE_PATH_KUBECLT,
        headers=auth_headers
    )

    return response_release_kubectl.text.replace('v', '')


def get_helm_latest_version():
    response_releases_helm = requests.get(
        LATEST_RELEASE_PATH_HELM,
        headers=auth_headers
    )

    release_helm_json_obj = json.loads(response_releases_helm.text)
    return release_helm_json_obj.get('tag_name').replace('v', '')


def get_velero_latest_version():
    response_releases_velero = requests.get(
        LATEST_RELEASE_PATH_VELERO,
        headers=auth_headers
    )

    release_velero_json_obj = json.loads(response_releases_velero.text)
    return release_velero_json_obj.get('tag_name').replace('v', '')


def get_argocd_latest_version():
    response_releases_argocd = requests.get(
        LATEST_RELEASE_PATH_ARGOCD,
        headers=auth_headers
    )

    release_argocd_json_obj = json.loads(response_releases_argocd.text)
    return release_argocd_json_obj.get('tag_name').replace('v', '')


def render_template(tag_kubectl=None, tag_helm=None, tag_velero=None, tag_argocd=None):
    # Generate Dockerfile template with new upstream version
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('Dockerfile.j2')
    filename = os.path.join(root, 'Dockerfile')

    with open(filename, 'w') as fh:
        fh.write(template.render(
            tag_kubectl = tag_kubectl or control['kubectl_version'],
            tag_helm = tag_helm or control['helm_version'],
            tag_velero = tag_velero or control['velero_version'],
            tag_argocd = tag_argocd or control['argocd_version']
        ))


def update_control(control):
    with open('control.json', 'w') as fh:
        fh.write(json.dumps(control))


def add_commit_push(commit_message):
    # Add and push changes to github repo
    with open('Dockerfile') as f:
        docker_file = f.read()

    with open('control.json') as f:
        control_file = f.read()

    # Connect to GitHub API and push the changes.
    github = github3.login(token=GITHUB_TOKEN)
    repository = github.repository_with_id(GITHUB_REPOSITORY_ID)

    github_dockerfile = repository.file_contents('/Dockerfile', ref=DEFAULT_BRANCH)
    github_control = repository.file_contents('/control.json', ref=DEFAULT_BRANCH)

    pushed_index_change = github_dockerfile.update(
        commit_message,
        docker_file.encode('utf-8'),
        branch=DEFAULT_BRANCH
    )

    pushed_control_change = github_control.update(
        'Update control ' + commit_message.replace('Bump ', ''),
        control_file.encode('utf-8'),
        branch=DEFAULT_BRANCH
    )

    print('Pushed commit {} to {} branch:\n    {}'.format(
        pushed_index_change['commit'].sha,
        DEFAULT_BRANCH,
        pushed_index_change['commit'].message,
    ))


def create_new_release(release_message):
    release_version = semver.parse(get_kube_tool_latest_version())
    release_version['patch'] = release_version['patch'] + 1

    #Create new release
    data = {
        'name': semver.format_version(**release_version),
        'tag_name': semver.format_version(**release_version),
        'body': release_message
    }

    headers = {
        'Authorization': 'token %s' % GITHUB_TOKEN,
        'Accept': 'application/vnd.github.v3+json'
    }
    print(data)

    response_new_release = requests.post(
        'https://api.github.com/repos/DNXLabs/docker-kube-tools/releases',
        data=json.dumps(data),
        headers=headers
    )


if __name__ == "__main__":
    # Kubectl
    kubectl_latest = get_kubectl_latest_version()
    print('Kubectl upstream version: %s' % kubectl_latest)
    print('DNX Kubectl version: %s' % control['kubectl_version'])
    if semver.compare(kubectl_latest, control['kubectl_version']) == 1:
        print('Rendering template for Kubectl.')
        render_template(tag_kubectl=kubectl_latest)
        control['kubectl_version'] = kubectl_latest
        update_control(control)
        commit_message = 'Bump Kubectl version to v%s' % kubectl_latest
        add_commit_push(commit_message)
        release_changes = True
        release_message += "- %s.\r\n" % commit_message
    else:
        print('Nothing to do, the upstream is in the same version or lower version.')

    print('--------------------------------')

    # Helm
    helm_latest = get_helm_latest_version()
    print('Helm upstream version: %s' % helm_latest)
    print('DNX Helm version: %s\n' % control['helm_version'])

    if semver.compare(helm_latest, control['helm_version']) == 1:
        print('Rendering template for Helm.')
        render_template(tag_helm=helm_latest)
        control['helm_version'] = helm_latest
        update_control(control)
        commit_message = 'Bump Helm version to v%s' % helm_latest
        add_commit_push(commit_message)
        release_changes = True
        release_message += "- %s.\r\n" % commit_message
    else:
        print('Nothing to do, the upstream is in the same version or lower version.')

    print('--------------------------------')

    # Velero
    velero_latest = get_velero_latest_version()
    print('Velero upstream version: %s' % velero_latest)
    print('DNX Velero version: %s\n' % control['velero_version'])

    if semver.compare(velero_latest, control['velero_version']) == 1:
        print('Rendering template for Velero.')
        render_template(tag_velero=velero_latest)
        control['velero_version'] = velero_latest
        update_control(control)
        commit_message = 'Bump Velero version to v%s' % velero_latest
        add_commit_push(commit_message)
        release_changes = True
        release_message += "- %s.\r\n" % commit_message
    else:
        print('Nothing to do, the upstream is in the same version or lower version.')

    print('--------------------------------')

    # Argo CD
    argocd_latest = get_argocd_latest_version()
    print('Argo CD upstream version: %s' % argocd_latest)
    print('DNX Argo CD version: %s\n' % control['argocd_version'])

    if semver.compare(argocd_latest, control['argocd_version']) == 1:
        print('Rendering template for Argo CD.')
        render_template(tag_argocd=argocd_latest)
        control['argocd_version'] = argocd_latest
        update_control(control)
        commit_message = 'Bump Argo CD version to v%s' % argocd_latest
        add_commit_push(commit_message)
        release_changes = True
        release_message += "- %s.\r\n" % commit_message
    else:
        print('Nothing to do, the upstream is in the same version or lower version.')

    if release_changes:
        create_new_release(release_message[:-4])