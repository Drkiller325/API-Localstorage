document.addEventListener('DOMContentLoaded', () => {
    const movieInput = document.getElementById('Task-input');
    const addMovieButton = document.getElementById('add-task');
    const movieList = document.getElementById('Task-list');

    // Load movies from local storage
    const movies = JSON.parse(localStorage.getItem('movies')) || [];

    // Render movies
    const renderMovies = () => {
        movieList.innerHTML = '';
        movies.forEach((movie, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${movie.name}
                <div>
                    <button class="like-button ${movie.liked ? 'liked' : ''}" data-index="${index}">
                        ${movie.liked ? '✅' : '✅︎'}
                    </button>
                    <button class="delete-button" data-index="${index}">❌</button>
                </div>
            `;
            movieList.appendChild(li);
        });
    };

    // Save movies to local storage
    const saveMovies = () => {
        localStorage.setItem('movies', JSON.stringify(movies));
    };

    // Add movie
    addMovieButton.addEventListener('click', () => {
        const movieName = movieInput.value.trim();
        if (movieName) {
            movies.push({ name: movieName, liked: false });
            movieInput.value = '';
            saveMovies();
            renderMovies();
        }
    });

    // Handle movie list clicks
    movieList.addEventListener('click', (event) => {
        if (event.target.classList.contains('like-button')) {
            const index = event.target.getAttribute('data-index');
            movies[index].liked = !movies[index].liked;
            saveMovies();
            renderMovies();
        } else if (event.target.classList.contains('delete-button')) {
            const index = event.target.getAttribute('data-index');
            movies.splice(index, 1);
            saveMovies();
            renderMovies();
        }
    });

    // Initial render
    renderMovies();
});