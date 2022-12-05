for id in $(docker ps -q)
  do                            
    if [[ $(docker port "${id}") == 5000 ]]; then
    echo "stopping container ${id}"
    docker stop "${id}"
  fi
 done
