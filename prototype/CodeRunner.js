function base64ToBytes(base64) {
    // This function is copied from https://developer.mozilla.org/en-US/docs/Glossary/Base64
    const binString = atob(base64);
    return Uint8Array.from(binString, (m) => m.codePointAt(0));
}

function bytesToBase64(bytes) {
    // This function is copied from https://developer.mozilla.org/en-US/docs/Glossary/Base64
    const binString = String.fromCodePoint(...bytes);
    return btoa(binString);
}