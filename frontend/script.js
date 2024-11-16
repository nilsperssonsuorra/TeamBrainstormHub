const ideaForm = document.getElementById('idea-form');
const ideasList = document.getElementById('ideas-list');

const IDEA_SERVICE_URL = 'http://localhost:30000/ideas';
const VOTING_SERVICE_URL = 'http://localhost:30001/vote';

// Fetch and display ideas
async function fetchIdeas() {
    const response = await fetch(IDEA_SERVICE_URL);
    const ideas = await response.json();
    ideasList.innerHTML = '';
    ideas.forEach(idea => {
        const ideaDiv = document.createElement('div');
        ideaDiv.className = 'idea';
        ideaDiv.innerHTML = `
            <h3>${idea.title}</h3>
            <p>${idea.description}</p>
            <p>Votes: <span id="votes-${idea.id}">${idea.votes}</span></p>
            <button class="vote-button" onclick="voteIdea(${idea.id})">Vote</button>
        `;
        ideasList.appendChild(ideaDiv);
    });
}

// Submit a new idea
ideaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    const response = await fetch(IDEA_SERVICE_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description })
    });

    if (response.ok) {
        ideaForm.reset();
        fetchIdeas();
    } else {
        alert('Failed to submit idea.');
    }
});

// Vote for an idea
async function voteIdea(id) {
    const response = await fetch(`${VOTING_SERVICE_URL}/${id}`, {
        method: 'POST'
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById(`votes-${id}`).innerText = data.votes;
    } else {
        alert('Failed to vote.');
    }
}

// Initial fetch
fetchIdeas();
