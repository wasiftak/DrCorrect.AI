const typingArea = document.getElementById('word-typing-area');
const aiOutput = document.getElementById('ai-output');
const suggestionsBox = document.getElementById('suggestions-box');

let currentWord = '';
let currentWordStartIndex = -1;

// --- 1. AUTOSUGGESTION LOGIC ---
typingArea.addEventListener('input', async (event) => {
    const text = typingArea.value;
    const caretPosition = typingArea.selectionStart;

    const textToCaret = text.substring(0, caretPosition);
    const words = textToCaret.split(/\s+/);
    currentWord = words[words.length - 1];
    currentWordStartIndex = textToCaret.lastIndexOf(currentWord);

    if (currentWord.length > 2) {
        const response = await fetch('/check_spelling', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word: currentWord }),
        });
        const data = await response.json();
        displaySuggestions(data.suggestions);
    } else {
        hideSuggestions();
    }
});

// --- 2. AUTOCORRECT LOGIC (ON SPACEBAR PRESS) ---
typingArea.addEventListener('keyup', (event) => {
    if (event.key === ' ' || event.code === 'Space') {
        const caretPosition = typingArea.selectionStart;
        const textBeforeCaret = typingArea.value.substring(0, caretPosition - 1);
        const wordStartIndex = textBeforeCaret.search(/\S+$/);

        if (wordStartIndex !== -1) {
            const wordToCorrect = textBeforeCaret.substring(wordStartIndex).replace(/[.,!?:;]$/, '');
            
            fetch('/check_spelling', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word: wordToCorrect }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.autocorrection) {
                    const fullText = typingArea.value;
                    const before = fullText.substring(0, wordStartIndex);
                    const after = fullText.substring(wordStartIndex + wordToCorrect.length);
                    
                    typingArea.value = before + data.autocorrection + after;
                    
                    const newCaretPosition = (before + data.autocorrection).length + 1;
                    typingArea.focus();
                    typingArea.setSelectionRange(newCaretPosition, newCaretPosition);
                }
            });
        }
    }
});

// --- HELPER FUNCTIONS ---
function displaySuggestions(suggestions) {
    if (suggestions && suggestions.length > 0) {
        suggestionsBox.innerHTML = '';
        suggestions.forEach((suggestion, index) => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            li.addEventListener('click', () => {
                acceptSuggestion(suggestion);
            });
            suggestionsBox.appendChild(li);
        });
        positionSuggestionsBox();
        suggestionsBox.style.display = 'block';
        suggestionsBox.children[0].classList.add('selected');
    } else {
        hideSuggestions();
    }
}

function hideSuggestions() {
    suggestionsBox.style.display = 'none';
}

function acceptSuggestion(suggestion) {
    const text = typingArea.value;
    const before = text.substring(0, currentWordStartIndex);
    const after = text.substring(currentWordStartIndex + currentWord.length);
    typingArea.value = before + suggestion + ' ' + after;
    hideSuggestions();
    typingArea.focus();
    const newCaretPosition = (before + suggestion).length + 1;
    typingArea.setSelectionRange(newCaretPosition, newCaretPosition);
}

function positionSuggestionsBox() {
    const lineHeight = 30;
    const lines = typingArea.value.substr(0, typingArea.selectionStart).split("\n").length;
    suggestionsBox.style.top = `${lines * lineHeight}px`;
    suggestionsBox.style.left = '15px';
}

// --- 3. KEYBOARD NAVIGATION ---
typingArea.addEventListener('keydown', (e) => {
    if (suggestionsBox.style.display === 'block') {
        const items = suggestionsBox.children;
        let selectedIndex = -1;
        for (let i = 0; i < items.length; i++) {
            if (items[i].classList.contains('selected')) {
                selectedIndex = i;
                break;
            }
        }

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (selectedIndex < items.length - 1) {
                if (selectedIndex !== -1) items[selectedIndex].classList.remove('selected');
                items[selectedIndex + 1].classList.add('selected');
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (selectedIndex > 0) {
                items[selectedIndex].classList.remove('selected');
                items[selectedIndex - 1].classList.add('selected');
            }
        } else if (e.key === 'Enter' || e.key === 'Tab') {
            e.preventDefault();
            if (selectedIndex !== -1) {
                acceptSuggestion(items[selectedIndex].textContent);
            }
        } else if (e.key === 'Escape') {
            hideSuggestions();
        }
    }
});

// --- 4. AI ASSISTANT (RIGHT-CLICK) ---
typingArea.addEventListener('contextmenu', (event) => {
    event.preventDefault();
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
        aiOutput.innerText = 'Analyzing...';
        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: selectedText }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                aiOutput.innerText = `Error: ${data.error}`;
            } else {
                aiOutput.innerText = data.result;
            }
        })
        .catch(error => {
            console.error('Analysis Error:', error);
            aiOutput.innerText = 'Failed to analyze text.';
        });
    }
});