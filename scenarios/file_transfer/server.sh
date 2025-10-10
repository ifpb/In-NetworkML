#!/usr/bin/env bash

set -euo pipefail

# Script configuration
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default configuration
readonly DEFAULT_TEST_DIR="/tmp/test_files"
readonly DEFAULT_FILE_SIZES="1M 10M 50M 100M" # 1MB, 10MB, 50MB, 100MB

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Global variables
TEST_DIR="${TEST_DIR:-$DEFAULT_TEST_DIR}"
FILE_SIZES="${FILE_SIZES:-$DEFAULT_FILE_SIZES}"

# Logging functions
log() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Display usage information
usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Create test files for SCP transfers.

Options:
    -d, --test-dir DIR      Directory for test files (default: $DEFAULT_TEST_DIR)
    -s, --sizes SIZES       File sizes to create (default: $DEFAULT_FILE_SIZES)
    -v, --verbose          Enable verbose output
    --help                 Show this help message

Environment variables:
    TEST_DIR, FILE_SIZES

Examples:
    $SCRIPT_NAME
    $SCRIPT_NAME -s "1M 10M 100M"
    FILE_SIZES="1M 10M" $SCRIPT_NAME
EOF
}

# Parse command line arguments
parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
    -d | --test-dir)
      TEST_DIR="$2"
      shift 2
      ;;
    -s | --sizes)
      FILE_SIZES="$2"
      shift 2
      ;;
    -v | --verbose)
      VERBOSE=true
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      log_error "Unknown option: $1"
      usage
      exit 1
      ;;
    esac
  done
}

# Validate environment and dependencies
validate_environment() {
  local errors=0

  # Check required commands
  for cmd in dd ssh scp; do
    if ! command -v "$cmd" &>/dev/null; then
      log_error "Required command '$cmd' not found"
      ((errors++))
    fi
  done

  # Validate file sizes format
  for size in $FILE_SIZES; do
    if [[ ! "$size" =~ ^[0-9]+[KMGT]?$ ]]; then
      log_error "Invalid file size format: $size (use formats like 1M, 10M, 1G)"
      ((errors++))
    fi
  done

  return $errors
}

# Convert size to bytes for verification
size_to_bytes() {
  local size=$1
  if [[ "$size" =~ ^[0-9]+[KMGTPEZY]?$ ]]; then
    local num=${size%[KMGTPEZY]}
    local unit=${size:${#num}}

    case $unit in
    K) echo $((num * 1024)) ;;
    M) echo $((num * 1024 * 1024)) ;;
    G) echo $((num * 1024 * 1024 * 1024)) ;;
    T) echo $((num * 1024 * 1024 * 1024 * 1024)) ;;
    *) echo $num ;; # bytes
    esac
  else
    echo 0
  fi
}

# Create test directory structure
create_test_directory() {
  log_info "Creating test directory: $TEST_DIR"

  if ! mkdir -p "$TEST_DIR"; then
    log_error "Failed to create test directory: $TEST_DIR"
    return 1
  fi

  # Create subdirectories for different file types
  mkdir -p "$TEST_DIR/text"
  mkdir -p "$TEST_DIR/binary"
  mkdir -p "$TEST_DIR/archive"

  log_success "Test directory structure created"
}

# Generate test files
generate_test_files() {
  log_info "Generating test files..."

  local files_created=0

  for size in $FILE_SIZES; do
    local text_file="$TEST_DIR/text/file_${size}.txt"
    local bin_file="$TEST_DIR/binary/file_${size}.bin"

    # Create text file with pattern
    if [[ ! -f "$text_file" ]]; then
      log_info "Creating text file: $(basename "$text_file")"
      if dd if=/dev/urandom of="$text_file" bs="$size" count=1 2>/dev/null; then
	((files_created++)) || true
	else
	  log_error "Failed to create text file: $(basename "$text_file")"
      fi
    else
      log_info "Text file already exists: $(basename "$text_file")"
    fi

    # Create binary file
    if [[ ! -f "$bin_file" ]]; then
      log_info "Creating binary file: $(basename "$bin_file")"
      if dd if=/dev/urandom of="$bin_file" bs="$size" count=1 2>/dev/null; then
        ((files_created++)) || true
      else
        log_error "Failed to create binary file: $(basename "$bin_file")"
      fi
    else
      log_info "Binary file already exists: $(basename "$bin_file")"
    fi
  done

  # Create archive files by combining multiple files
  local archive_file="$TEST_DIR/archive/mixed_files.tar.gz"
  if [[ ! -f "$archive_file" ]]; then
    log_info "Creating archive file: $(basename "$archive_file")"
    if tar czf "$archive_file" -C "$TEST_DIR/text" . -C "$TEST_DIR/binary" . 2>/dev/null; then
      ((files_created++)) || true
    else
      log_warning "Failed to create archive file"
    fi
  fi

  log_success "Generated $files_created test files"
}

# Verify test files
verify_test_files() {
  log_info "Verifying test files..."

  local errors=0

  for size in $FILE_SIZES; do
    local text_file="$TEST_DIR/text/file_${size}.txt"
    local bin_file="$TEST_DIR/binary/file_${size}.bin"
    local target_bytes=$(size_to_bytes "$size")

    for file in "$text_file" "$bin_file"; do
      if [[ -f "$file" ]]; then
        local actual_size=$(stat -c%s "$file" 2>/dev/null || echo 0)
        if [[ $actual_size -ne $target_bytes ]]; then
          log_error "File size mismatch: $(basename "$file") (expected: $target_bytes, actual: $actual_size)"
          ((errors++))
        elif [[ "${VERBOSE:-false}" == "true" ]]; then
          log_info "$(basename "$file"): $actual_bytes bytes"
        fi
      else
        log_error "File not found: $(basename "$file")"
        ((errors++))
      fi
    done
  done

  if [[ $errors -eq 0 ]]; then
    log_success "All test files verified successfully"
  else
    log_error "Found $errors file verification errors"
    return 1
  fi
}

# Main execution function
main() {
  log_info "Starting SCP test file generator"

  parse_arguments "$@"

  if ! validate_environment; then
    log_error "Environment validation failed"
    exit 1
  fi

  # Create test files
  create_test_directory
  generate_test_files
  verify_test_files
}

main $@
