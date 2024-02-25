const modalBtns=document.getElementsByClassName("modal-button")
const modalBody=document.getElementById('modal-body')
const startBtn=document.getElementById('start-btn')
const quizBox=document.getElementById('quiz-box')
const scoreBox=document.getElementById('score-box')
const resultBox=document.getElementById('result-box')
const timerBox=document.getElementById('timer-box')
let timer; 


const activateTimer = (time)=>{
    if (time.toString().length<2){
        timerBox.innerHTML=`<b>0${time}:00</b>`
    }else{
        timerBox.innerHTML=`<b>${time}:00</b>`
    }
    let minutes=time-1
    let seconds=60
    let displaySecond
    let displayMinute
    timer=setInterval(()=>{
        seconds--
        if (seconds<0){
            seconds=59
            minutes--
        }
        if (minutes.toString().length<2){
            displayMinute='0'+minutes
        }
        else{
            displayMinute=minutes
        }
        if(seconds.toString().length<2){
            displaySecond='0'+seconds
        }
        else{
            displaySecond=seconds
        }
        if(minutes===0 && seconds===0){
            timerBox.innerHTML="<b>00:00</b>"
            setTimeout((timer)=>{
                clearInterval(timer)
                alert("Time Over")
                sendData()
            },500)
            
            
        }
        timerBox.innerHTML=`<b>${displayMinute}:${displaySecond}</b>`
    },1000)
    //to actually get the ex -2 min 1.59 min
}


let data
const url=window.location.href

Array.from(modalBtns).forEach(btn => {
    btn.addEventListener('click', () => {
        const pk = btn.getAttribute('data-pk');
        const name = btn.getAttribute('data-quiz');
        const numQuestions = btn.getAttribute('data-questions');
        const time = btn.getAttribute('data-time');
        const pass = btn.getAttribute('data-pass');

        modalBody.innerHTML=`
        <div class="h5 mb-3">Are you Sure you want to begin <b>${name}</b></div>
        <div class="text-muted">
    <ul>
        <li>number of questions:<b>${numQuestions}</b></li>
        <li>score to pass:<b>${pass}%</b></li>
        <li>time:<b>${time} minutes</b></li>
        
    </ul>
</div>
        `
        startBtn.addEventListener('click',()=>{
            window.location.href=url+pk
        })
    });
});

$.ajax({
    type:'GET',
    url:`${url}data`,
    success:function(response){
        // console.log(response)
        const data=response.data
        data.forEach(el=>{
            for(const [question,answers] of Object.entries(el))
            {
                quizBox.innerHTML+=`
                
                <div class="my-3 cl-black">
                <b>${question}</b>
                </div>
                <hr>`
                answers.forEach(answer=>{
                    quizBox.innerHTML+=`
                    <div>
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for="${question}">${answer}</label>
                    </div>
                    `
                })
            }
        })
        // activateTimer(response.time)
        activateTimer(response.time);

        quizForm.addEventListener('submit', e => {
            e.preventDefault();
            
            // Clear the timer when the form is submitted
            clearInterval(timer);
            timerBox.innerHTML="<b>submitted</b>"
            
            sendData();
        });

        
    },
    error:function(error){
        console.log(error)
    } 
})

const quizForm=document.getElementById('quiz-form')
const csrf=document.getElementsByName('csrfmiddlewaretoken')


const sendData=()=>{
    const elements=[...document.getElementsByClassName('ans')]
    const data={}
    data['csrfmiddlewaretoken']=csrf[0].value
    elements.forEach(el=>{
        if (el.checked){
            data[el.name]=el.value
        }
        else{
            if(!data[el.name]){
                data[el.name]=null
            }
        }
    })
    $.ajax({
        type:'POST',
        url:`${url}save/`,
        data:data,
        success:function(response){
            const results=response.result
            console.log(results)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML=`${response.passed ? 'Congratulations':'Ups..:( '} Your result is ${response.score}%`
            results.forEach(res=>{
                const resDiv=document.createElement('div')
                for(const [question,resp] of Object.entries(res)){
                    // console.log(question)
                    // console.log(resp)
                    // console.log("*****")
                    resDiv.innerHTML+=question
                    const cls=['container','p-2','m-2']
                    resDiv.classList.add(...cls)
                    if (resp=="not_answered"){
                        resDiv.innerHTML+=" -not answered"
                        resDiv.classList.add("cl-danger")
                    }
                    else{
                        const answer=resp['answered']
                        const correct=resp['correct_answer']

                        if (answer==correct){
                            resDiv.classList.add('cl-success')
                            resDiv.innerHTML+=` answered:${answer}`
                        }
                        else{
                            resDiv.classList.add('cl-danger')
                            resDiv.innerHTML+=`| correct answer: ${correct} | answered: ${answer}`
                           
                            
                        }

                    }
                }
                // const body=document.getElementById('quiz-ans')
                resultBox.append(resDiv)
                timerBox.innerHTML="<b>00:00</b>"
                clearInterval(timer);
            });
            
        },
        error:function(error){
            console.log(error)
        }

    })

}
