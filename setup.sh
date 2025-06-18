#!/usr/bin/env bash

# Universal setup script for Fish shell and Bash/Zsh
# This script detects the current shell and adapts accordingly

# Function to detect the current shell
detect_shell() {
    if [ -n "$FISH_VERSION" ]; then
        echo "fish"
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    elif [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    else
        echo "unknown"
    fi
}

# Function to check if python3 is available
check_python3() {
    if ! command -v python3 &> /dev/null; then
        echo "Error: python3 is not installed. Please install Python 3 first."
        exit 1
    fi
}

# Function to create virtual environment
create_venv() {
    python3 -m venv .venv
    
    if [ ! -d ".venv" ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
}

# Function to activate virtual environment based on shell
activate_venv() {
    local shell_type=$1
    
    case $shell_type in
        "fish")
            source .venv/bin/activate.fish
            ;;
        "bash"|"zsh")
            source .venv/bin/activate
            ;;
        *)
            echo "Warning: Unknown shell type. You may need to activate the virtual environment manually."
            ;;
    esac
}

# Function to create .env file based on shell
create_env_file() {
    local shell_type=$1
    
    if [ ! -f ".env" ]; then
        echo "Creating .env file..."
        echo "# Get these from https://my.telegram.org/apps" > .env
        
        case $shell_type in
            "fish")
                echo "set -x TELEGRAM_API_ID your_api_id_here" >> .env
                echo "set -x TELEGRAM_API_HASH your_api_hash_here" >> .env
                echo "" >> .env
                echo "# Download directory (optional - leave empty for default)" >> .env
                echo "set -x TELEGRAM_DOWNLOAD_PATH ~/Downloads/telegram" >> .env
                ;;
            "bash"|"zsh")
                echo "TELEGRAM_API_ID=your_api_id_here" >> .env
                echo "TELEGRAM_API_HASH=your_api_hash_here" >> .env
                echo "" >> .env
                echo "# Download directory (optional - leave empty for default)" >> .env
                echo "TELEGRAM_DOWNLOAD_PATH=~/Downloads/telegram" >> .env
                ;;
        esac
        
        echo "Please edit the .env file with your Telegram API credentials"
    fi
}

# Function to show activation instructions based on shell
show_instructions() {
    local shell_type=$1
    
    echo "Virtual environment setup complete!"
    echo ""
    echo "To activate the environment, run:"
    
    case $shell_type in
        "fish")
            echo "source .venv/bin/activate.fish"
            echo ""
            echo "To run the downloader, run:"
            echo "source .env && python3 telegram_media_downloader.py"
            ;;
        "bash"|"zsh")
            echo "source .venv/bin/activate"
            echo ""
            echo "To run the downloader, run:"
            echo "export \$(cat .env | xargs) && python3 telegram_media_downloader.py"
            ;;
    esac
    
    echo ""
    echo "To deactivate the environment when done, run:"
    echo "deactivate"
}

# Main execution
main() {
    local current_shell=$(detect_shell)
    
    echo "Detected shell: $current_shell"
    echo "Setting up Telegram Media Downloader..."
    echo ""
    
    # Check Python3
    check_python3
    
    # Create virtual environment
    create_venv
    
    # Activate virtual environment
    activate_venv "$current_shell"
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    # Create .env file
    create_env_file "$current_shell"
    
    # Show instructions
    show_instructions "$current_shell"
}

# Run main function
main "$@" 