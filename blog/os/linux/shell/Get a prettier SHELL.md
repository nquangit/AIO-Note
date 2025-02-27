# Get a prettier SHELL

![Cover Image](https://images.unsplash.com/photo-1629654297299-c8506221ca97)

## Z Shell (zsh)

### Key Features

1. **Interactive Shell:** Zsh provides a highly interactive shell experience with features like advanced tab completion, spelling correction, and syntax highlighting.
2. **Extensive Customization:** Users can customize Zsh to suit their preferences and workflow by configuring various options and settings. This includes defining aliases, customizing prompt appearance, and setting up plugins and themes.
3. **Powerful Tab Completion:** Zsh's tab completion is highly sophisticated and can complete commands, filenames, options, and even suggest completions based on the context.
4. **Plugin System:** Zsh has a rich ecosystem of plugins and extensions that add additional functionality and integrations with other tools and frameworks.
5. **Advanced Scripting:** Zsh supports advanced scripting features, including associative arrays, parameter expansion, and various control structures, making it suitable for writing complex shell scripts.

### Install

- **Check current SHELL:**

    ```shell
    echo $SHELL
    ```

    > **If the output is `/usr/bin/zsh`, you do not need to reinstall. Proceed to install OhMyZsh.**

- **On Ubuntu/Debian:**

    ```shell
    sudo apt update
    sudo apt install zsh
    ```

- **On CentOS/RHEL:**

    ```shell
    sudo yum install zsh
    ```

- **On macOS using Homebrew:**

    ```shell
    brew install zsh
    ```

### Verify

- After installation, you can verify if Zsh is installed by running:

    ```shell
    zsh --version
    ```

### Set Zsh as Default Shell

- Set Zsh as the default shell:

    ```bash
    chsh -s $(which zsh)
    ```

    > For the changes to take effect, log out of your shell session and log back in or restart your computer.

## Oh My Zsh

> Oh My Zsh is a delightful, open-source, community-driven framework for managing your Zsh configuration. It comes bundled with thousands of helpful functions, helpers, plugins, themes, and more.

[OhMyZsh's homepage](https://ohmyz.sh/#install)

### Install

- Install OhMyZsh with `curl`:

    ```bash
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```

- Or with `wget`:

    ```bash
    sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
    ```

### Theme

- You can use any theme from Zsh by manually setting it in the Zsh profile file `~/.zshrc`.  
For example:

```text
ZSH_THEME="robbyrussell" # Edit this line
```

### Plugin

> You can also use Plugins depending on your purposes and preferences.

[OhMyZsh Plugins Wiki](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins)


## Powerlevel10k

> Powerlevel10k is a theme for Zsh. It emphasizes [speed](https://github.com/romkatv/powerlevel10k#uncompromising-performance), [flexibility](https://github.com/romkatv/powerlevel10k#extremely-customizable), and [out-of-the-box experience](https://github.com/romkatv/powerlevel10k#configuration-wizard).

### Install Fonts

1. Download the fonts:
   - [MesloLGS NF Regular.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf)
   - [MesloLGS NF Bold.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf)
   - [MesloLGS NF Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf)
   - [MesloLGS NF Bold Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf)

2. Install the fonts by right-clicking and selecting "Install," or copy the font files to:
   - `~/.local/share/fonts` (for a user-specific installation)  
   - `/usr/local/share/fonts` (for a system-wide installation)

3. Start the Powerlevel10k installation:

   - Clone the repository:

    ```shell
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
    ```

   - Set `ZSH_THEME="powerlevel10k/powerlevel10k"` in `~/.zshrc`.

   - Reload the Zsh profile:

    ```shell
    source ~/.zshrc
    ```

    **Note:** It will start asking you some questions to customize your shell. Choose according to your preferences.

4. In the final step - **Instant Prompt Mode**, choose option (3) **Off**.

5. Done!
