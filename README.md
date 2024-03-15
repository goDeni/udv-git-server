# Commands

Сборка
```bash
podman build -t git-server .
```

Запуск
```bash
podman run \
    --rm \
    --network host \
    --name git-server \
    -v $(pwd)/.workdir/reps-dir:/git \
    -v $(pwd)/server/nginx.conf:/etc/nginx/nginx.conf \
    git-server
```

Остановка
```bash
podman stop git-server
```

Перезапуск
```bash
podman restart git-server
```

Логи
```bash
podman logs -f git-server
```