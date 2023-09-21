#Checkpoint: Caio Vinícius, Henrique Koji, Luana Bannwart, Guilherme Cavalheiro



import docker
import requests

# Conecte-se ao Docker usando o socket Unix local
client = docker.DockerClient(base_url='tcp://0.0.0.0:2375')


def listar_containers():
    containers = client.containers.list()
    if containers:
        for container in containers:
            print(f'ID: {container.id}, Nome: {container.name}, Status: {container.status}')
    else:
        print('Não há containers em execução.')


def listar_imagens():
    images = client.images.list()
    if images:
        for image in images:
            print(f'ID: {image.id}, Nome: {image.tags}')
    else:
        print('Não há imagens disponíveis.')


def criar_container():
    image_name = input('Digite o nome da sua imagem Docker: ')
    container_name = input('Digite o nome do seu container (letras minúsculas): ')
    command = input('Digite o comando para iniciar o seu container (opcional): ')

    try:
        container = client.containers.create(
            image=image_name,
            name=container_name,
            command=command
        )
        print(f'Container criado. ID: {container.id}')
    except docker.errors.ImageNotFound:
        print(f'Imagem Docker com nome {image_name} não encontrada.')


def iniciar_container():
    container_id = input('Digite o ID do container que deseja iniciar: ')
    try:
        container = client.containers.get(container_id)
        container.start()
        print(f'Container {container_id} iniciado com sucesso.')
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def parar_container():
    container_id = input('Digite o ID do container que deseja parar: ')
    try:
        container = client.containers.get(container_id)
        container.stop()
        print(f'Container {container_id} parado com sucesso.')
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def reiniciar_container():
    container_id = input('Digite o ID do container que deseja reiniciar: ')
    try:
        container = client.containers.get(container_id)
        container.restart()
        print(f'Container {container_id} reiniciado com sucesso.')
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def matar_container():
    container_id = input('Digite o ID do container que deseja matar: ')
    try:
        container = client.containers.get(container_id)
        container.kill()
        print(f'Container {container_id} morto com sucesso.')
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def remover_container():
    container_id = input('Digite o ID do container que deseja remover: ')
    try:
        container = client.containers.get(container_id)
        if container.status == 'running':
            container.stop()
            print(f'Container {container_id} parado com sucesso antes de remover.')
        container.remove()
        print(f'Container {container_id} removido com sucesso.')
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def listar_processos(container_id):
    try:
        container = client.containers.get(container_id)
        processes = container.top(ps_args='aux')
        print('\n'.join(processes['Titles']))
        for process in processes['Processes']:
            print(process)
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def obter_logs(container_id):
    try:
        container = client.containers.get(container_id)
        logs = container.logs().decode('utf-8')
        print(logs)
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def listar_images():
    images = client.images.list()
    if images:
        for image in images:
            print(f'ID: {image.id}, Tags: {image.tags}')
    else:
        print('Não há imagens disponíveis.')


def remover_image():
    image_id = input('Digite o ID da imagem que deseja remover: ')
    try:
        client.images.remove(image_id)
        print(f'Imagem com ID {image_id} removida com sucesso.')
    except docker.errors.ImageNotFound:
        print(f'Imagem com ID {image_id} não encontrada.')


def obter_informacoes_do_sistema():
    info = client.info()
    print(f'ID do Docker Daemon: {info["ID"]}')
    print(f'Versão do Docker: {info["ServerVersion"]}')
    print(f'Sistema Operacional: {info["OperatingSystem"]}')
    print(f'Arquitetura do Sistema: {info["Architecture"]}')
    print(f'Número de CPUs: {info["NCPU"]}')
    print(f'Memória Total: {info["MemTotal"]}')


def ping():
    response = requests.get('http://0.0.0.0:2375/_ping')
    if response.status_code == 200:
        print('O servidor Docker está acessível.')
    else:
        print('O servidor Docker não está acessível.')


def obter_dados_de_uso(container_id):
    try:
        container = client.containers.get(container_id)
        stats = client.api.stats(container_id, decode=True)
        for stat in stats:
            print(f'Uso de CPU: {stat["cpu_stats"]["cpu_usage"]["total_usage"]}')
            print(f'Uso de Memória: {stat["memory_stats"]["usage"]}')
            break  # Mostrar apenas a primeira leitura
    except docker.errors.NotFound:
        print(f'Container com ID {container_id} não encontrado.')


def obter_versao():
    version = client.version()
    print(f'Versão do Docker API: {version["ApiVersion"]}')
    print(f'Versão do Docker: {version["Version"]}')


# Menu principal
while True:
    print("\nOpções:")
    print("1. Listar Containers")
    print("2. Criar Container")
    print("3. Iniciar Container")
    print("4. Parar Container")
    print("5. Reiniciar Container")
    print("6. Matar Container")
    print("7. Remover Container")
    print("8. Listar Processos em um Container")
    print("9. Obter Logs de um Container")
    print("10. Listar Imagens")
    print("11. Remover Imagem")
    print("12. Obter Informações do Sistema")
    print("13. Ping do Docker Daemon")
    print("14. Obter Dados de Uso de um Container")
    print("15. Obter Versão do Docker")
    print("16. Sair")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        listar_containers()
    elif escolha == '2':
        criar_container()
    elif escolha == '3':
        iniciar_container()
    elif escolha == '4':
        parar_container()
    elif escolha == '5':
        reiniciar_container()
    elif escolha == '6':
        matar_container()
    elif escolha == '7':
        remover_container()
    elif escolha == '8':
        container_id = input('Digite o ID do container: ')
        listar_processos(container_id)
    elif escolha == '9':
        container_id = input('Digite o ID do container: ')
        obter_logs(container_id)
    elif escolha == '10':
        listar_images()
    elif escolha == '11':
        remover_image()
    elif escolha == '12':
        obter_informacoes_do_sistema()
    elif escolha == '13':
        ping()
    elif escolha == '14':
        container_id = input('Digite o ID do container: ')
        obter_dados_de_uso(container_id)
    elif escolha == '15':
        obter_versao()
    elif escolha == '16':
        break
    else:
        print('Opção inválida. Tente novamente.')
