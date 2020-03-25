# Object recognizer

[**Cleuton Sampaio**](https://github.com/cleuton)

[**ENGLISH VERSION HERE**](./english.md)

[![](./banner_livros2.png)](https://www.lcm.com.br/site/#livros/busca?term=cleuton)

## Instalação da OpenCV em Raspberry PI 3

Não adianta tentar instalar a OpenCV com pip! Existem repositórios criados para ARM, mas a maioria não tem versão para armhf. As arquiteturas arm são: 

- **arm64**: Versão 64 bits da especificação ARM. Em teoria, o Raspberry PI 3 suporta arm64, mas o sistema operacional padrão, o [**Raspbian**](https://www.raspberrypi.org/downloads/), não;
- **armhf**: Versão da especificação ARM de 32 Bits (versão 7). É suportada pelo Raspbian;

Se você tiver um Raspberry PI 3 com Raspbian, provavelmente estará usando arquitetura 32 bits, portanto, os repositórios para ARM, como o [**piwheels**](https://www.piwheels.org/), não possuem versão do OpenCV disponível.

Resumo: Você terá que compilar a OpenCV 4 para seu Raspberry. E nem pense em fazer [**cross-compile**](https://visualgdb.com/tutorials/raspberry/opencv/build/) em seu PC e instalar em seu Raspberry, pois não vai funcionar com a OpenCV!

Relaxe! Você tem ai pelo menos 4 horas de trabalho para instalar a OpenCV 4 no seu RPIII.

## Preparação

O site [**PyImageSearch**](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) tem um guia muito bom e que funciona perfeitamente com Raspberry PI 3 com Raspbian. Siga-o. Vou listar aqui os principais passos. 

Se você vai instalar diretamente usando seu RPIII ou se vai usar via ssh, a escolha é sua. Via SSH, vocẽ tem que habilitar o SSH usando o raspi-config: 

1. Digite: ```sudo raspi-config`` no terminal;
2. Selecione: **Interfacing Options**;
3. Navegue e selecione **SSH**;
4. Escolha: **Yes**;
5. Selecione: **Ok**;
6. Escolha: **Finish**;

Você está usando um micro SD como disco do seu RPIII, certo? Espero que seja maior que 8GB, caso contrário, poderá ter problemas. 

É necessário expandir o sistema de arquivos para usar todo o cartão SD e isso deve ser feito antes de iniciar a instalação: 

1. Digite: ```sudo raspi-config```;
2. Escolha: ```Advanced Options```;
3. Escolha: ```Expand filesystem```;
4. Tecle: **ENTER**;
5. Escolha: ```Finish```;
6. Faça reboot no RPIII.

Eu recomendaria um SD card de pelo menos 32GB!

Eu recomendaria fortemente a instalação do **Miniconda**: 

```
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
md5sum Miniconda3-latest-Linux-armv7l.sh
bash Miniconda3-latest-Linux-armv7l.sh
source ~/.bashrc
```

Agora, você pode instalar o Python 3.6: 

```
conda install python=3.6
```

Você pode criar um ambiente virtual com o seu miniconda, mas, na verdade, eu o uso sem ambiente mesmo. Só para caso eu precise mudar a versão do Python ou coisa semelhante.

## Dependências

A OpenCV tem muitas dependências, e precisamos começar a instalar. Antes de mais nada, rode: 

```
sudo apt-get update && sudo apt-get upgrade
```

Agora, instale as ferramentas de desenvolvimento: 

```
sudo apt-get install build-essential cmake unzip pkg-config
```

Agora, as bibliotecas de vídeo: 

```
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
```
A biblioteca GUI GTK: 

```
sudo apt-get install libgtk-3-dev
```

Uma biblioteca para reduzir os warnings GTK: 

```
sudo apt-get install libcanberra-gtk*
```

Otimizações numéricas: 

```
sudo apt-get install libatlas-base-dev gfortran
```

Os headers de desenvolvimento do Python: 

```
sudo apt-get install python3-dev
```
Vamos baixar os fontes da OpenCV e da OpenCV-contrib: 

```
cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
```

Descompacte e renomeie: 

```
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib
```

Instale a biblioteca [**numpy**]:
```
pip install numpy
```

Agora, vamos criar a pasta **build**:
```
cd ~/opencv
mkdir build
cd build
```

Finalmente, vamos começar o build em si. Atenção, uma alteração no **CMakelists.txt** é necessária: 

1. Abra um terminal para o seu RPIII (SSH ou não);
2. Edite o arquivo: "~/opencv/CMakeLists.txt";
3. Logo após os comentários iniciais, inclua as linhas abaixo: 
```
set(PYTHON_EXECUTABLE "$ENV{HOME}/miniconda3/bin/python3.6")
set(PYTHON_LIBRARIES "$ENV{HOME}/miniconda3/lib/libpython3.6m.so")
set(PYTHON_INCLUDE_PATH "$ENV{HOME}/miniconda3/include/python3.6m")
```
Se você seguiu minhas orientações, então os caminhos devem estar corretos. Verifique na sua pasta "~/miniconda3".

O comando para invocar o **CMake** que eu usei é este: 

```
cmake -DPYTHON_DEFAULT_EXECUTABLE=$(which python3) -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..
```
Na verdade, você só estará preparando o build. Depois que o comando terminar, recomendo você aumentar (temporariamente) a memória de swap do RPIII: 

1. Digite: ```sudo nano /etc/dphys-swapfile```;
2. Encontre a linha: ```CONF_SWAPSIZE=...``` (anote o valor que estava);
3. Modifique para : ```CONF_SWAPSIZE=2048```;
4. Salve o arquivo;
5. Pare o serviço de swap: ```sudo /etc/init.d/dphys-swapfile stop```;
6. Reinicie o serviço de swap: ```sudo /etc/init.d/dphys-swapfile start```;

**Atenção**: Assim que terminar de rodar o build (comando "make"), desfaça estes passos! Volte o valor original, pare e reinicie o serviço de swap. Isso é para preservar a duração do seu SD card!

Agora, inicie o build: 
```
make -j4
```

Relaxe! Isso vai demorar MUUUUUUUUIIIIIIIIIITTTTTOOOOOO. Vai dar alguns warnings, mas persista! Ao final, você verá essa mensagem: 

```
...
[100%] Linking CXX shared module ../../lib/cv2.so
[100%] Built target opencv_python2
[100%] Linking CXX shared module ../../lib/python3/cv2.cpython-36m-arm-linux-gnueabihf.so
[100%] Built target opencv_python3
```

Terminou? Ótimo! Agora, vamos instalar: 

```
sudo make install
sudo ldconfig
```

Só falta uma coisa: Criar um link simbólico da lib OpenCV dentro do **miniconda3**: 

```
cd ~/miniconda3/lib
sudo ln -s /usr/local/python/cv2/python-3.6/cv2.cpython-36m-arm-linux-gnueabihf.so
```

Agora é simples: 
```
python
>>> import cv2
>>>
```
Se não der problema, seu opencv-python está ok. 

Ah, e coloque a seguinte linha no seu arquivo: "~/.bashrc": 
```
export PYTHONPATH=/home/pi/miniconda3/lib:$PYTHONPATH
```

## Outras dependências

Bom, o projeto depende de outras coisas. Você pode criar um ambiente Conda com o arquivo [**env-armhf.yml**](./armhf.yml) ou pode instalar manualmente: 

```
pip install picamera
pip install gtts
pip install python-vlc
pip install RPi.GPIO
```



