# Steps:

- Init Next.js with `npx create-next-app@latest --ts` (See [Next.js with TypeScript](https://nextjs.org/docs/basic-features/typescript))

  > Also see [Next.js Upgrade Guide](https://nextjs.org/docs/upgrading)

- Move code to `src` folder and add `@` paths

  - Move files:
    ```bash
    mkdir src
    git mv pages src/
    git mv styles src/
    ```
  - Update `tsconfig.json`:
    ```json
    {
      "compilerOptions": {
        // ...
        "baseUrl": ".",
        "paths": {
          "@/*": ["./src/*"],
          "@/public/*": ["./public/*"]
        }
      },
      "include": ["next-env.d.ts", "src/**/*.ts", "src/**/*.tsx"]
    }
    ```

- Install [typescript-plugin-css-modules](https://github.com/mrmckeb/typescript-plugin-css-modules#installation) for better IDE experience with CSS Modules

- Install [Airbnb Style](https://github.com/airbnb/javascript) with `npx install-peerdeps --dev eslint-config-airbnb`  
  and enhance it with [TypeScript support](https://github.com/iamturns/eslint-config-airbnb-typescript).  
  Also update eslintrc:

  ```json
  {
    "extends": ["airbnb", "airbnb-typescript", "next/core-web-vitals"],
    "parserOptions": {
      "project": "./tsconfig.json"
    },
    "rules": {}
  }
  ```

- Add `.vscode/extensions.json` file (and install the extensions)

- Config VSCode to auto-fix eslint problems.  
  In `.vscode/settings.json`:

  ```json
  {
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": true
    }
  }
  ```

- Add [Sass Support](https://nextjs.org/docs/basic-features/built-in-css-support#sass-support)
  with `npm install sass`, and rename `.css` files to `.scss`

  ```bash
  git mv src/styles/globals.css src/styles/globals.css
  git mv src/styles/Home.module.css src/styles/Home.module.css
  ```

- Stylelint:

  - Install [Stylelint](https://stylelint.io/user-guide/get-started) with `stylelint-config-standard-scss`
  - Add [Stylelint VSCode extension](https://marketplace.visualstudio.com/items?itemName=stylelint.vscode-stylelint)
  - Config VSCode to auto-fix Stylelint problems in `.vscode/settings.json`:
    ```json
    {
      "editor.codeActionsOnSave": {
        "source.fixAll.stylelint": true
      }
    }
    ```
  - Disable VSCode's default CSS linting and use Stylelint instead.  
    In `.vscode/settings.json`:
    ```json
    {
      "css.validate": false,
      "scss.validate": false,
      "less.validate": false,
      "stylelint.validate": ["css", "scss"]
    }
    ```
  - Update `package.json`:
    ```json
    {
      "scripts": {
        "lint:eslint": "next lint",
        "lint:stylelint": "stylelint \"src/**/*.{css,scss}\" --ignore-path .gitignore",
        "lint": "npm run lint:eslint && npm run lint:stylelint"
      }
    }
    ```
  - Config Stylelint to work with Tailwind.  
    In `stylelint.config.js`:
    ```javascript
    module.exports = {
      rules: {
        "scss/at-rule-no-unknown": [
          true,
          {
            ignoreAtRules: [
              "tailwind",
              "apply",
              "variants",
              "responsive",
              "screen",
              "layer",
            ],
          },
        ],
      },
    };
    ```

- Prettier:

  - Install [Prettier](https://prettier.io/) with `npm install --save-dev --save-exact prettier`
  - Add `.prettierrc.js` and `.prettierignore` files
  - Add [Prettier VSCode extension](https://marketplace.visualstudio.com/items?itemName=SimonSiefke.prettier-vscode)
  - Config VSCode to auto-format CSS files with Prettier in `.vscode/settings.json`:
    ```json
    "[css][scss]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "editor.formatOnSave": true
    }
    ```

  > Some people decide to install [eslint-config-prettier](https://github.com/prettier/eslint-config-prettier)
  > to make ESLint and Prettier work together  
  > (See [Next.js Usage With Prettier](https://nextjs.org/docs/basic-features/eslint#prettier)
  > and [Prettier: Integrating with Linters](https://prettier.io/docs/en/integrating-with-linters.html)).
  > \
  > \
  > We didn't do it in this template because Prettier is very strict and we want to keep some freedom.
  > We use Prettier on CSS and assets files but not on Code files.

- Tailwind CSS:

  - [Install Tailwind CSS](https://tailwindcss.com/docs/guides/nextjs).
  - In `tailwind.config.js` make sure you use the paths `./src/app/...` and `./src/components/...`
  - Install formatter for Tailwind classes: [Tailwind CSS Prettier Plugin](https://github.com/tailwindlabs/prettier-plugin-tailwindcss)

- Install [clsx](https://github.com/lukeed/clsx) to toggle classes. See [Next.js Styling Tips](https://nextjs.org/learn/basics/assets-metadata-css/styling-tips)
- Install [axios](https://github.com/axios/axios) and [SWR](https://swr.vercel.app), and set api architecture

- Install [lodash](https://lodash.com) with `npm install lodash` and `npm install --save-dev @types/lodash`

- Add [.env files](https://nextjs.org/docs/basic-features/environment-variables)

- Add Dockerfile and docker-compose.yml
