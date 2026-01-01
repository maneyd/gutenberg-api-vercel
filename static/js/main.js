let currentPage = 1;
let totalCount = 0;
const itemsPerPage = 25;

const filterIds = ['book_id', 'title', 'author', 'topic', 'language', 'mime_type'];

function getFilters() {
    const filters = {};
    filterIds.forEach(id => {
        const element = document.getElementById(id);
        filters[id] = element ? element.value.trim() : '';
    });
    return filters;
}

function buildQueryString(filters, page) {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
        if (filters[key]) {
            params.append(key, filters[key]);
        }
    });
    params.append('page', page);
    return params.toString();
}

function updateURL(filters, page) {
    const queryString = buildQueryString(filters, page);
    const newURL = '/api/books' + (queryString ? '?' + queryString : '');
    window.history.pushState({}, '', newURL);
}

function showLoading(show) {
    const loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = show ? 'block' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    if (message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
}

function formatArray(arr, defaultText) {
    return arr && arr.length > 0 ? arr.join(', ') : defaultText;
}

function formatAuthors(authors) {
    if (!authors || authors.length === 0) return 'Unknown';
    return authors.map(a => a.name).join(', ');
}

function formatDownloadLinks(links) {
    if (!links || links.length === 0) return 'None';
    return links.map(link => 
        '<a href="' + link.url + '" target="_blank">' + link.mime_type + '</a>'
    ).join(' ');
}

function createBookCard(book, serialNumber) {
    const bookCard = document.createElement('div');
    bookCard.className = 'book-card';
    
    bookCard.innerHTML = 
        '<div class="book-serial">' + serialNumber + '</div>' +
        '<div class="book-title">' + (book.title || 'Untitled') + '</div>' +
        '<div class="book-id">ID: ' + book.id + '</div>' +
        '<div class="book-detail"><strong>Authors:</strong> ' + formatAuthors(book.authors) + '</div>' +
        '<div class="book-detail"><strong>Language:</strong> ' + (book.language || 'Unknown') + '</div>' +
        '<div class="book-detail"><strong>Subjects:</strong> ' + formatArray(book.subjects, 'None') + '</div>' +
        '<div class="book-detail"><strong>Bookshelves:</strong> ' + formatArray(book.bookshelves, 'None') + '</div>' +
        '<div class="book-detail"><strong>Download Links:</strong> ' + formatDownloadLinks(book.download_links) + '</div>';
    
    return bookCard;
}

function updatePagination(totalPages) {
    const pagination = document.getElementById('pagination');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');
    
    if (totalPages > 1) {
        pagination.style.display = 'block';
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        pageInfo.textContent = 'Page ' + currentPage + ' of ' + totalPages;
    } else {
        pagination.style.display = 'none';
    }
}

function displayBooks(data) {
    const container = document.getElementById('booksContainer');
    const resultsInfo = document.getElementById('resultsInfo');
    
    totalCount = data.count || 0;
    
    if (totalCount === 0) {
        container.innerHTML = '<div class="no-results">No books found.</div>';
        resultsInfo.textContent = 'No results found.';
        document.getElementById('pagination').style.display = 'none';
        return;
    }
    
    const totalPages = Math.ceil(totalCount / itemsPerPage);
    const startSerial = (currentPage - 1) * itemsPerPage + 1;
    
    resultsInfo.textContent = 'Found ' + totalCount + ' book(s) - Page ' + currentPage + ' of ' + totalPages;
    
    updatePagination(totalPages);
    
    container.innerHTML = '';
    
    data.results.forEach((book, index) => {
        const serialNumber = startSerial + index;
        const bookCard = createBookCard(book, serialNumber);
        container.appendChild(bookCard);
    });
}

async function searchBooks(page) {
    if (!page) {
        page = 1;
    }
    currentPage = page;
    const filters = getFilters();
    const queryString = buildQueryString(filters, currentPage);
    
    updateURL(filters, currentPage);
    
    showLoading(true);
    showError('');
    
    try {
        const response = await fetch('/api/books?' + queryString);
        const data = await response.json();
        
        if (response.ok) {
            displayBooks(data);
        } else {
            showError(data.error || 'An error occurred.');
            document.getElementById('booksContainer').innerHTML = '';
        }
    } catch (error) {
        showError('Failed to connect to server.');
        document.getElementById('booksContainer').innerHTML = '';
    } finally {
        showLoading(false);
    }
}

function changePage(direction) {
    const newPage = currentPage + direction;
    if (newPage >= 1) {
        searchBooks(newPage);
    }
}

function clearFilters() {
    filterIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.value = '';
    });
    
    currentPage = 1;
    document.getElementById('booksContainer').innerHTML = '';
    document.getElementById('resultsInfo').textContent = '';
    document.getElementById('pagination').style.display = 'none';
    showError('');
    
    window.history.pushState({}, '', window.location.pathname);
}

document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.filter-group input');
    inputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                currentPage = 1;
                searchBooks(1);
            }
        });
    });
});
