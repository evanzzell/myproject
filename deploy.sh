#!/bin/bash

# Файли деплойментів та служб
WEB_DEPLOYMENT=web-deployment.yaml
WEB_SERVICE=web-service.yaml
MONGO_DEPLOYMENT=mongo-deployment.yaml
MONGO_SERVICE=mongo-service.yaml
MONGO_PVC=mongo-pvc.yaml

# Масив з файлами деплойментів та служб
declare -a arr=(
    $WEB_DEPLOYMENT
    $WEB_SERVICE
    $MONGO_DEPLOYMENT
    $MONGO_SERVICE
    $MONGO_PVC
)
# Функція перевірки існування файлу
check_file_exists() {
    if [ ! -f $1 ]; then
        printf "File not found: %s\n" "$1"
        exit 1
    fi
}

# Функція застосування конфігурацій
apply_services() {
    for i in "${arr[@]}"; do 
        check_file_exists $i
        echo "Applying $i..."
        kubectl apply -f $i
        if [ $? -ne 0 ]; then
            echo "Failed to apply $i"
            exit 1
        fi
    done
}

# Функція видалення конфігурацій
delete_services() {
    for i in "${arr[@]}"; do 
        check_file_exists $i
        echo "Deleting $i..."
        kubectl delete -f $i
        if [ $? -ne 0 ]; then
            echo "Failed to delete $i"
            exit 1
        fi
    done
}

# Функція обробки аргументів
parse_arguments() {
    case "$1" in
        -r | --run )
            apply_services
            ;;
        -d | --delete )
            delete_services
            ;;
        * )
            echo "Usage: $0 {-r|--run|-d|--delete}"
            exit 1
            ;;
    esac
    shift
}

# Виклик функції обробки аргументів з переданими аргументами
parse_arguments "$@"
