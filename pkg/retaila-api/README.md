# Investra API
Full implementation of Investra communications.

## Heroku deploy
To deploy the heroku, commit first and after:
'git subtree push --prefix pkg/investra-api/ heroku master'

To check is the heroku deploy is succeeded:
'heroku ps:scale web=1'

To see the logs of the heroku deploy
'heroku logs'

To open de heroku web:
'heroku open'