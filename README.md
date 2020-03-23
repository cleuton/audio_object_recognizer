# Object recognizer

[**Cleuton Sampaio**](https://github.com/cleuton)

[**ENGLISH VERSION HERE**](./english.md)

[![](./banner_livros2.png)](https://www.lcm.com.br/site/#livros/busca?term=cleuton)

Clique na imagem para ver uma demonstração em vídeo: 
[![](./results.jpg)](https://youtu.be/eVmNh9URYuU)

Estou desenvolvendo um aparelho para reconhecer objetos à frente, dizer seus nomes e também informar a distância do objeto mais próximo. A ideia é criar algo que funcione para pessoas com dificuldades visuais. 

Se vai ser um dispositivo embarcado (um Raspberry etc) ou apenas um aplicativo de celular, ainda não sei. Mas estou selecionando e testando vários modelos. Nesta demonstração, estou utilizando o Yolo (You Only Look Once), com python e OpenCV. Me inspirei no artigo de [**Adrian Rosebrock**](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/) para criar esta PoC. 

Já testei com modelos CNN em Keras, usando bancos como o [**CIFAR**](https://www.cs.toronto.edu/~kriz/cifar.html) e o [**COCODataset**](http://cocodataset.org/#home), mas a performance do Yolo é melhor, embora seja menos preciso. 

Ainda é um projeto inacabado, mas resolvi compartilhar para vocês me ajudarem e desenvolverem suas próprias soluções. 

Estou usando a biblioteca [**gTTS**](https://gtts.readthedocs.io/en/latest/) da Google para transcrever texto em áudio. 

## Instalação

Clone o projeto Darknet (git clone https://github.com/pjreddie/darknet) e copie os arquivos abaixo para a pasta **yolo** deste projeto: 
- darknet/cfg/yolov3.cfg
- darknet/data/coco.names

Clique [**neste link**](https://pjreddie.com/media/files/yolov3.weights) e baixe o arquivo yolov3.weights, colocando na pasta **yolo** do projeto.


Instale o [**VLC**](https://www.videolan.org/vlc/). É melhor se você tiver o [**Anaconda**](https://anaconda.org/) também instalado, bastando criar um ambiente virtual com o comando: 

```
conda env create -f ./env.yml
conda activate object
```

Para executar, basta rodar o script [**simple_detector.py**]: 

```
python simple_detector.py
```

Se quiser, pode passar o caminho de um arquivo de imagem para testar. Eu anexei 2 imagens para você testar.

Ah, e eu criei um Dicionário JSON para traduzir os nomes dos objetos encontrados, incluindo o plural.





