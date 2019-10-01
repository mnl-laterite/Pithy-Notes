/**
 * Div element that will contain the notes.
 */
const notesContainer = document.getElementById('notes-container');
/**
 * Constant that records which note is currently selected.
 */
var selectedNoteId;

let logoutButton = document.getElementById('logout');
logoutButton.addEventListener('click', event => {

    // create a POST request to '/logout' when the button has been clicked
    let request = new XMLHttpRequest();
    request.open('POST', '/logout', true);
    request.onload = function () {
        document.location.reload();
    }
    request.send();

});

let newNoteButton = document.getElementById('newnote');
newNoteButton.addEventListener('click', newNote);

let saveNoteButton = document.getElementById('save-note-button');
saveNoteButton.addEventListener('click', saveNote);

let searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', searchButtonClicked);

let searchField = document.getElementById('to-search');
searchField.addEventListener('keyup', searchInitiated);

/**
 * Make a POST request to '/notes' when the 'New Note' butten is clicked 
 * and render the new note if the request was successfully handled.
 */
function newNote() {

    let request = new XMLHttpRequest();
    request.open('POST', '/notes', true);
    request.onload = function() {

        let data = JSON.parse(this.responseText);
        if (request.status == 200) {
            renderData(data);            
        }

    };

    request.send();
}

/**
 * If a note is selected, make a POST request to '/notes/<note_id>' when the 'Save Note' button is clicked.
 * Otherwise, make a POST request to '/notes/null' to create a new note with the current values of the editor 
 * and title field.
 */
function saveNote() {

    let title = document.getElementById('tentative-title').value;
    let contents = editor.getValue();
    let responseJSON = {"Title": title, "Contents": contents};
    let request = new XMLHttpRequest();
    let saveNoteId = selectedNoteId;

    if (saveNoteId) {
        
        request.open('POST', '/notes/'.concat(saveNoteId), true);
        request.setRequestHeader("Content-Type", "application/json");

        request.onload = function() {
            
            if (title) {
                // edit the note title in the page to reflect the changes
                let toEdit = document.getElementById(saveNoteId).getElementsByClassName('note-title')[0];
                toEdit.textContent = title;
            }

        };

        request.send(JSON.stringify(responseJSON));

    } else {

        request.open('POST', '/notes/null', true);
        request.setRequestHeader("Content-Type", "application/json");

        request.onload = function() {

            let data = JSON.parse(this.responseText);
            if (request.status == 200) {
                // render the new note in the page and mark it as the currently selected one
                renderData(data);
                selectedNoteId = data._id['$oid'];
                document.getElementById(selectedNoteId).style.background = "#d9fc9f";            
            }

        };

        request.send(JSON.stringify(responseJSON));
    }
}

/**
 * Make a PUT request to '/notes' with the search string the user has inputted.
 * Render the result in the page.
 */
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

/**
 * Double searchNoteClicked when the user presses the 'Enter' key in the seach note field.
 * @param {keyup} event 
 */
function searchInitiated(event) {

    if (event.key === "Enter") {
        searchButtonClicked();
    }
}

/**
 * Mark the clicked on note as the currently selected one and display its contents in the editor by making a 
 * GET request to '/notes/<note_id>' to retrieve the note contents.
 * @param {click} event 
 */
function noteClicked(event) {

    let previouslySelectedNoteId = selectedNoteId;
    selectedNoteId = event.currentTarget.id;

    if (previouslySelectedNoteId) {
        // a note was previously selected, so mark it as unselected before marking a new one as selected
        let exSelection = document.getElementById(previouslySelectedNoteId);
        if (exSelection) {
            exSelection.style.background = "#ffffff";
        }
    }
    // mark the clicked on note as the currently selected one
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

/**
 * Make a DELETE request to '/notes/<note_id>' to delete the currently selected/clicked on note
 * from the database, then clean the page of the elements associated with it.
 * @param {click} event 
 */
function deleteButtonClicked(event) {

    let noteId = event.currentTarget.id;

    let request = new XMLHttpRequest();
    request.open('DELETE', '/notes/'.concat(noteId), true);
    request.onload = function() {

        let elementToDelete = document.getElementById(noteId);
        notesContainer.removeChild(elementToDelete);
        selectedNoteId = null;
        editor.setValue("\n\n");
        document.getElementById('tentative-title').value = "";

    };

    request.send();
}

/**
 * Render the note data in the page. 
 * @param {JSON} data 
 */
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

/**
 * Make a GET request to '/notes' to retrieve all the notes the user has made and render the results
 * in the page. 
 */
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
