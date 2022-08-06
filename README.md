Meu nome é Alexandre Beck, fiz essa rest API para o processo seletivo de estágio no coco bambu como desenvolvedor.
Como nunca tive experiência com criações de API's, tive dificuldades de utilizar os tipos de dados, 'Enumeration' e 'timestamp', inclusive deixei comentado.

Para executar a api, utilizei o pipenv com o virtualenv. E para testar os endpoints utilizei o Postman http://localhost:5000/order.

o banco de dados foi criado manualmente por comandos dentro do python shell: 
    from delivery_api import db
    db.create_all()
    exit()