function toggleBlock(blockName) {
    const likeBlock = document.getElementById('likeBlock');
    const commentsBlock = document.getElementById('commentsBlock');
    const shareBlock = document.getElementById('shareBlock');
    // const likeBtn = document.getElementById('likeBtn');
    const commentsBtn = document.getElementById('commentsBtn');
    const shareBtn = document.getElementById('shareBtn');
    const elements = [[commentsBlock, commentsBtn], [shareBlock, shareBtn]];
    elements.forEach((el) => {
            // console.log(el);
            if (!el[0].classList.contains('hidden')) {
                if (el[0].id !== `${blockName}Block`) {
                    el[0].classList.add('hidden');
                    el[1].classList.remove(`button__${blockName}__pressed`);
                }

            }
        }
    )
    const element = document.getElementById(`${blockName}Block`);
    const button = document.getElementById(`${blockName}Btn`);
    button.classList.toggle(`button__${blockName}__pressed`);
    element.classList.toggle('hidden');
}


// const footerController = new FooterController();
// const likeBtn = document.getElementById('likeBtn');
const commentsBtn = document.getElementById('commentsBtn');
const shareBtn = document.getElementById('shareBtn');
// likeBtn.addEventListener('click', () => {
//     toggleBlock('like')
// });
commentsBtn.addEventListener('click', () => {
    toggleBlock('comments')
});
shareBtn.addEventListener('click', () => {
    toggleBlock('share')
});


function selectComment(commentId) {
    console.log(commentId)
    const comment = document.getElementById(commentId)
    comment.classList.toggle('box-reply-to')
    setTimeout(() => {
        comment.classList.toggle('box-reply-to');
    }, 800)
}

function like(postId) {
    fetch(`/api/v1/posts/${postId}/like/`, {method: 'POST'})
        .then((response) => {
            console.log(response);
            const setLikeBtn = document.getElementById('setLikeBtn');
            setLikeBtn.classList.toggle('button__like__pressed')
            return response.json();
        })
        .then((data)=>{
            const likesCount = document.getElementById('likesCount');
            likesCount.innerHTML = data.likes;
        });
}

// держать в самом конце файла
const textArea = document.getElementById('addCommentText')
textArea.addEventListener('focusin', () => {
    textArea.setAttribute('rows', 8)
})
// textArea.addEventListener('focusout', () => {
//     textArea.setAttribute('rows', 1)
// })