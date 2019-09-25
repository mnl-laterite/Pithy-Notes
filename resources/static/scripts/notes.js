const notesContainer = document.getElementById('notes-container');
const editorContainer = document.getElementById('editor-container');
var selectedNoteId;


let logoutButton = document.getElementById('logout');
logoutButton.addEventListener('click', event => {

    let request = new XMLHttpRequest();
    request.open('POST', '/logout', true);
    request.onload = function () {
        document.location.reload();
    }
    request.send();

});

let newNoteButton = document.getElementById('newnote');
newNoteButton.addEventListener('click', event => {

    let request = new XMLHttpRequest();
    request.open('POST', '/notes', true);
    request.onload = function() {

        let data = JSON.parse(this.responseText);
        if (request.status == 200) {
            renderData(data);
        }

    };

    request.send();
    
});

let saveNoteButton = document.getElementById('save-note-button');
saveNoteButton.addEventListener('click', event => {

    if (selectedNoteId) {
        let title = document.getElementById('tentative-title').value;
        let contents = editor.getValue();
        let responseJSON = {"Title": title, "Contents": contents};

        let request = new XMLHttpRequest();
        request.open('POST', '/notes/'.concat(selectedNoteId), true);
        request.setRequestHeader("Content-Type", "application/json");

        request.onload = function() {
            
            if (title) {
                console.log("Are we here?")
                let toEdit = document.getElementById(selectedNoteId).getElementsByClassName('note-title')[0];
                toEdit.textContent = title;
            }

        };

        request.send(JSON.stringify(responseJSON));
    }

});

let searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', searchButtonClicked);

function searchButtonClicked() {

    let searchString = document.getElementById('to-search').value;
    let searchJSON = {"Search": searchString}

    let request = new XMLHttpRequest();
    request.open('PUT', '/notes', true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function() {

        let foundNotes = JSON.parse(this.responseText);

        if (request.status == 200) {
            notesContainer.innerHTML = '';
            foundNotes.forEach(noteJSON => renderData(noteJSON));
        }

    };

    request.send(JSON.stringify(searchJSON));

}


function noteClicked(event) {

    let previouslySelectedNoteId = selectedNoteId;
    selectedNoteId = event.currentTarget.id;

    if (previouslySelectedNoteId) {
        let exSelection = document.getElementById(previouslySelectedNoteId);
        if (exSelection) {
            exSelection.style.background = "#ffffff";
        }
    }
    document.getElementById(selectedNoteId).style.background = "#d9fc9f";
    
    let request = new XMLHttpRequest();
    request.open('GET', '/notes/'.concat(selectedNoteId), true);
    request.onload = function() {

        let data = JSON.parse(this.responseText);
        if (request.status == 200) {
            
            if (data) {
                editor.setValue(data.Contents);
                document.getElementById('tentative-title').value = data.Title;
            }
        }

    };

    request.send();
}

function deleteButtonClicked(event) {

    let noteId = event.currentTarget.id;

    let request = new XMLHttpRequest();
    request.open('DELETE', '/notes/'.concat(noteId), true);
    request.onload = function() {

        let elementToDelete = document.getElementById(noteId);
        notesContainer.removeChild(elementToDelete);

    };

    request.send();

}

function renderData(data) {

    const id = data._id['$oid'];

    const note = document.createElement('div');
    note.setAttribute('class', 'note');
    note.setAttribute('id', id);

    const p = document.createElement('p');

    const titleSpan = document.createElement('span');
    titleSpan.setAttribute('class', 'note-title');
    titleSpan.textContent = data.Title;

    const space = document.createElement('br');

    const dateSpan = document.createElement('span');
    dateSpan.setAttribute('class', 'date');
    dateSpan.textContent = new Date(data.Time);

    const deleteButton = document.createElement('button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('id', id)
    deleteButton.innerText = "Delete Note";

    p.appendChild(titleSpan);
    p.appendChild(space);
    p.appendChild(dateSpan);
    note.appendChild(p);
    note.appendChild(deleteButton);
    notesContainer.insertBefore(note, notesContainer.firstChild);

    deleteButton.addEventListener('click', deleteButtonClicked);
    note.addEventListener('click', noteClicked);
    
}

function getNotes() {

    let request = new XMLHttpRequest();
    request.open('GET', '/notes', true);
    request.onload = function () {

        let notes = JSON.parse(this.responseText);
        if (request.status == 200) {
            notes.forEach(noteJSON => renderData(noteJSON));
        }

    };

    request.send();
}

getNotes();
