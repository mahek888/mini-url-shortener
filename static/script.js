const copyButton = document.getElementById("copyBtn");

if (copyButton) {

    copyButton.addEventListener("click", () => {

        const shortLink =
            document.getElementById("shortLink").textContent;

        navigator.clipboard.writeText(shortLink);

        const originalText = copyButton.textContent;

        copyButton.textContent = "✓ Copied";

        copyButton.disabled = true;

        setTimeout(() => {

            copyButton.textContent = originalText;

            copyButton.disabled = false;

        }, 2000);

    });

}