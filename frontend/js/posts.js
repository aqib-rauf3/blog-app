// Load posts on homepage
async function loadPosts() {
    const featuredContainer = document.getElementById('featured-posts-container');
    const recentContainer = document.getElementById('recent-posts-container');
    
    if (!featuredContainer && !recentContainer) return;
    
    try {
        const response = await fetch('http://localhost:5001/api/posts');
        const data = await response.json();
        
        if (data.posts && data.posts.length > 0) {
            // Display featured posts (first 3)
            if (featuredContainer) {
                let featuredHTML = '';
                data.posts.slice(0, 3).forEach(post => {
                    featuredHTML += `
                    <div class="post-card">
                        <div class="post-image">
                            <i class="fas fa-newspaper"></i>
                        </div>
                        <div class="post-content">
                            <div class="post-meta">
                                <span class="post-author">By ${post.author_name}</span>
                                <span class="post-date">${formatDate(post.created_at)}</span>
                            </div>
                            <h3 class="post-title">${post.title}</h3>
                            <p class="post-excerpt">${post.content.substring(0, 150)}...</p>
                            <a href="#" class="read-more" onclick="viewPost(${post.id})">
                                Read More <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                    `;
                });
                featuredContainer.innerHTML = featuredHTML;
            }
            
            // Display recent posts (all)
            if (recentContainer) {
                let recentHTML = '';
                data.posts.forEach(post => {
                    recentHTML += `
                    <div class="recent-post">
                        <h4>${post.title}</h4>
                        <p>${post.content.substring(0, 100)}...</p>
                        <div class="recent-meta">
                            <span>By ${post.author_name}</span>
                            <a href="#" onclick="viewPost(${post.id})">Read</a>
                        </div>
                    </div>
                    `;
                });
                recentContainer.innerHTML = recentHTML;
            }
        } else {
            if (featuredContainer) {
                featuredContainer.innerHTML = '<p class="no-posts">No posts available yet.</p>';
            }
            if (recentContainer) {
                recentContainer.innerHTML = '<p class="no-posts">No posts available yet.</p>';
            }
        }
    } catch (error) {
        console.error('Error loading posts:', error);
        if (featuredContainer) {
            featuredContainer.innerHTML = '<p class="error">Error loading posts. Please try again later.</p>';
        }
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// View single post
function viewPost(postId) {
    alert('View post ' + postId + ' - This would navigate to post detail page');
}
