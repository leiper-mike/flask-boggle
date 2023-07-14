
let guessed = []
$("#btn").on("click", submitGuess)
async function submitGuess(evt){
    evt.preventDefault()
    const guess = $("#input")[0].value
    const resp = await axios.get(`/checkword`, { 
        params: {
            guess: guess
        }
    })
    console.log(resp)
    let msg;
    if(resp.data.result == "ok" && !guessed.includes(guess)){
        msg = `Great Job! You earned ${guess.length} points!`
        const newPoints = Number($("#points")[0].innerText) + guess.length
        $("#points")[0].innerText = newPoints
        guessed.push(guess);
    }
    else if (resp.data.result == "not-on-board")
        msg = "Could not find word on board, try again!"
    else if (resp.data.result == "not-a-word") {
        msg = "That's not a word I have in my dictonary, try again!"
    }
    else{
        msg = "You already guessed that word! Try again!"
    }
    $("#msg")[0].innerText = msg;
    $("#input")[0].value = "";
}
let time = 60
const timer = setInterval(function (){
    time--;
    if(time <= 0){
        stopGame();
        clearInterval(timer);
    }
    $("#timer")[0].innerText = time;
}, 1000)

async function stopGame(){
    $("#btn")[0].disabled = true
    await axios.post('/score', {
        score: Number($("#points")[0].innerText)
    })
    guessed = []
}