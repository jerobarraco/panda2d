TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

SOURCES +=

include(deployment.pri)
qtcAddDeployment()

DISTFILES += \
    run.py \
    test.py \
    panda2d_xml/xmlDao.py \
    panda2d_xml/__init__.py \
    panda2d_xml/old_tiles.py \
    panda2d_xml/sprites.py \
    panda2d_xml/tiles.py \
    data/cat1.png \
    data/cat3.png \
    data/cat4.png \
    data/newSpriteSheet.png \
    data/spritesheet.png \
    data/spritesheet.animations \
    data/newSpriteSheet.sprites \
    data/spritesheet.sprites \
    catsu/main.py \
    catsu/models.py \
    data/newAnimation.anim

