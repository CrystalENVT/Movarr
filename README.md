# Movarr
Monitors directory for complete seasons (or movies) & moves to appropriate media directory. Output Rulesets are currently: Movies, Shows, Anime (Movies + Shows)

![Trans Rights](https://pride-badges.pony.workers.dev/static/v1?label=Trans%20Rights!&stripeWidth=6&stripeColors=5BCEFA,F5A9B8,FFFFFF,F5A9B8,5BCEFA)
![Made By Humans](https://img.shields.io/badge/Made%20by-Humans-008000?labelColor=00BB00&color=grey)  
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/crystalenvt/movarr/main_flow.yaml?branch=main)
![Docker Pulls](https://img.shields.io/docker/pulls/crystalenvt/movarr)  
![GitHub commits since latest release](https://img.shields.io/github/commits-since/crystalenvt/movarr/latest) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/crystalenvt/movarr/main)

## How to run
### CLI via Python
```bash
cp .env.sample .env
# Edit .env for your configuration
python3.14 -m venv venv
source venv/bin/activate
python ./movarr.py
```

### Via Docker Compose
Use the `DockerCompose.yaml` example, & utilize the .env file

## Configuration Options
| Config Option |    Value     |      Details      |
| ------------- | ------------ | ----------------- |
| tmdb_v4_read_access_token | \<\<Bearer Token\>\> | Sign-up for API here: https://www.themoviedb.org/settings/api |
| run_schedule | */5 * * * * | Crontab style expression |
| input_directories | /tmp/input | Use semicolon to track multiple directories |
| movie_output_directory | /tmp/movies | |
| tv_output_directory | /tmp/tv | |
| anime_movie_output_directory | /tmp/anime_movies | |
| anime_tv_output_directory | /tmp/anime_tv | |
| include_specials | false | Enable this if your library is expecting specials to exist |
| DEBUG | false | Enable additional debug logs |
| docker_mount_point | /tmp/data | Docker(Compose) only ENV var |
