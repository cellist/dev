-- Create example data manually, execute like so:
-- psql -a -f populate.sql

DROP TABLE public.examples;
DROP TABLE public.tags;
DROP TABLE public.translations;

CREATE TABLE public.examples (
    id     SERIAL      PRIMARY KEY,
    akey   VARCHAR(10) NOT NULL,
    avalue VARCHAR(10) NOT NULL
);

CREATE TABLE public.tags (
    id       SERIAL      PRIMARY KEY,
    aconcept VARCHAR(25) NOT NULL,
    atag     VARCHAR(25) NOT NULL
);

CREATE TABLE public.translations (
    id       SERIAL      PRIMARY KEY,
    transfrom VARCHAR(20) NOT NULL,
    transto   VARCHAR(20) NOT NULL,
    fromterm  VARCHAR(30) NOT NULL,
    toterm    VARCHAR(30) NOT NULL
);

INSERT INTO
    public.examples (akey,avalue)
VALUES
    ('key1','val1'),
    ('key2','val2'),
    ('key3','val3');

INSERT INTO
    public.tags (aconcept,atag)
VALUES
    ('fruit','concrete'),
    ('banana','fruit'),
    ('banana','colour-yellow'),
    ('pineapple','fruit'),
    ('pineapple','colour-yellow'),
    ('cherry','fruit'),
    ('cherry','colour-red'),
    ('apple','fruit'),
    ('apple','colour-green'),
    ('kiwi','fruit'),
    ('kiwi','colour-green'),
    ('orange','fruit'),
    ('orange','colour-orange'),
    ('strawberry','fruit'),
    ('strawberry','colour-red'),
    ('date','fruit'),
    ('date','colour-brown'),
    ('blueberry','fruit'),
    ('blueberry','colour-blue'),
    ('music-instrument','concrete'),
    ('violin','music-instrument'),
    ('violin','semi-polyphonic'),
    ('viola','music-instrument'),
    ('viola','semi-polyphonic'),
    ('cello','music-instrument'),
    ('cello','semi-polyphonic'),
    ('piano','music-instrument'),
    ('piano','polyphonic'),
    ('organ','music-instrument'),
    ('organ','polyphonic'),
    ('guitar','music-instrument'),
    ('guitar','polyphonic'),
    ('flute','music-instrument'),
    ('flute','monophonic'),
    ('clarinet','music-instrument'),
    ('clarinet','monophonic'),
    ('electronic-device','concrete'),
    ('smartphone','electronic-device'),
    ('laptop','electronic-device'),
    ('tablet pc','electronic-device'),
    ('programming-language','abstract'),
    ('C++','programming-language'),
    ('C++','compiler'),
    ('C++','object-oriented'),
    ('Python','programming-language'),
    ('Python','interpreter'),
    ('Python','object-oriented'),
    ('Python','functional'),
    ('Java','programming-language'),
    ('Java','interpreter'),
    ('Java','object-oriented'),
    ('Smalltalk','programming-language'),
    ('Smalltalk','interpreter'),
    ('Smalltalk','object-oriented'),
    ('Lisp','programming-language'),
    ('Lisp','interpreter'),
    ('Lisp','functional'),
    ('Pascal','programming-language'),
    ('Pascal','compiler'),
    ('Pascal','procedural'),
    ('Prolog','programming-language'),
    ('Prolog','interpreter'),
    ('operating-system','abstract'),
    ('MS Windows','operating-system'),
    ('MS Windows','commercial'),
    ('IBM OS/2','operating-system'),
    ('IBM OS/2','commercial'),
    ('Minix','operating-system'),
    ('Minix','free'),
    ('Linux','operating-system'),
    ('Linux','free'),
    ('The Hurd','operating-system'),
    ('The Hurd','free'),
    ('FreeBSD','operating-system'),
    ('FreeBSD','free'),
    ('ReactOS','operating-system'),
    ('ReactOS','free'),
    ('Mac OS','operating-system'),
    ('Mac OS','commercial');

INSERT INTO
    public.translations (transfrom,transto,fromterm,toterm)
VALUES
    ('Latin','German','alea','Wuerfel'),
    ('Latin','German','deus','Gott'),
    ('Latin','German','machina','Maschine'),
    ('Latin','German','aeroplanus','Flugzeug'),
    ('English', 'Latin', 'peace', 'pax'),
    ('English', 'Latin', 'cock', 'gallus'),
    ('English', 'Latin', 'dog', 'canis'),
    ('English', 'Latin', 'horse', 'equus'),
    ('English', 'Latin', 'room', 'camera'),
    ('English', 'Latin', 'table', 'mensa'),
    ('French', 'English', 'matin', 'morning'),
    ('French', 'English', 'soir', 'evening'),
    ('French', 'English', 'amour', 'love'),
    ('French', 'English', 'eau', 'water'),
    ('French', 'English', 'cygne', 'swan'),
    ('German', 'French', 'Dirigent', 'conducteur'),
    ('German', 'French', 'Schauspielerin', 'actrice'),
    ('German', 'French', 'Welt', 'monde'),
    ('German', 'French', 'Tod', 'mort'),
    ('German', 'French', 'Hund', 'cien');
