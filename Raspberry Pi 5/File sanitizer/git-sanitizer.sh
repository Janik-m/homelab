function git-sanitize() {
  if [ -z "$1" ]; then
    echo "Usage: git-sanitize <file>"
    return 1
  fi

  echo "--> Sending $1 to Ollama Sanitizer..."

  EXT="${1##*.}"
  BASENAME="${1%.*}"

  # Wersja bez jq, bo n8n zwraca teraz Text, a nie JSON
  curl -s -X POST -F "data=@$1" "http://<IP_ADDRESS>:5678/webhook/sanitize" > "${BASENAME}_SAFE.${EXT}"

  echo "--> Done! Result saved in: ${BASENAME}_SAFE.${EXT}"
}