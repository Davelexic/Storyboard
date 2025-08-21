# Node.js Setup Guide for Cinei-Reader

## Current Status
❌ Node.js is not currently installed or available in the PATH.

## Required for Client Development
The client is a React Native application that requires Node.js for:
- Package management (npm)
- Running development server
- Building and testing the app
- Running linting tools

## Installation Steps

### Option 1: Official Node.js Installer (Recommended)
1. Visit https://nodejs.org/
2. Download the LTS version (currently 18.x or 20.x)
3. Run the installer and follow the setup wizard
4. Restart your terminal/command prompt
5. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Option 2: Using Node Version Manager (Advanced)
For developers who need to manage multiple Node.js versions:

**Windows (nvm-windows):**
1. Download from https://github.com/coreybutler/nvm-windows
2. Install and restart terminal
3. Install Node.js LTS:
   ```bash
   nvm install --lts
   nvm use --lts
   ```

## React Native Development Requirements
Based on the project's package.json, you'll also need:
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development on macOS)

## Post-Installation Setup
Once Node.js is installed:

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Verify the setup by running tests:
   ```bash
   npm test
   ```

## Current Project Dependencies
- React Native: 0.71.0
- React: 18.2.0
- AsyncStorage: ^1.21.0

## Next Steps After Installation
1. Install React Native CLI globally: `npm install -g @react-native-community/cli`
2. Set up Android development environment
3. Run the development server: `npm start`
4. Test on device/emulator: `npm run android` or `npm run ios`

## Troubleshooting
- If Node.js commands aren't recognized, restart your terminal
- Check that Node.js is added to your system PATH
- For React Native issues, refer to https://reactnative.dev/docs/environment-setup
