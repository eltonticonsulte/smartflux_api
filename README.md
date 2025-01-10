# smartflux_api

docker network create smartflux_network

#dev
git config --local user.name "eltonticonsulte" --replace-all
git config --local user.email "elton@ticonsulte.com.br" --replace-all

#insta depende lamba
pip install -t dependencies -r requirements.txt
zipar dependencies + aplicacao aws_lambida_artifact.zip



https://api-read.smartflux.com.br/v1/visitor/daily?year=2025&month=01&day=06
{
  "hora": "16:00",
  "people_in": 600,
  "people_out": 589
}
