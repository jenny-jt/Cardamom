const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;
const useParams = ReactRouterDOM.useParams;
const useHistory = ReactRouterDOM.useHistory;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;


function Homepage() {
  return <div> Welcome to my site </div>
}

function LogIn() { 

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  function handleLogin(evt) {
    evt.preventDefault();

    const data = { 
      email: email,
      password: password
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    fetch('/api/login', options)
    .then(response => response.json())
    .then(data => {
      if (data === 'User logged in successfully') {
        alert(data)
      } else { 
        alert("incorrect email/password")
      }
    })
  }

  function handleEmailChange(evt) {
    setEmail(evt.target.value)
  }

  function handlePasswordChange(evt) {
    setPassword(evt.target.value)
  }

  return (
    <React.Fragment>
      <form onSubmit={handleLogin}>
        Email:
        <input value={email} onChange={handleEmailChange} type="text"></input>
        Password:
        <input value={password} onChange={handlePasswordChange} type="text"></input>
        <a href="/authorize"> Authorize with Google </a>
        <button> Log In </button>  
      </form>
    </React.Fragment>
  )  
}

  //   function handleSubmit(evt){
  //     evt.preventDefault()
  //     console.log(productName, company,productUrl,description,selectedBCorp,'selecteddepartment=',selectedDepartment,'selectedCerts:', certsForFilter,'user_id',userFromStorage.id, 'file=',file)
  //     let data = {productName:productName, company:company, productUrl:productUrl, description:description, selectedBCorp:selectedBCorp,category:selectedDepartment, selectedCerts:certsForFilter,user_id:userFromStorage.id, img:file }
  //     fetch('/add-product',{method: "POST",  body: JSON.stringify(data),  headers: {
  //       'Content-Type': 'application/json'}} )
  //     .then(response => response.json())
  //     .then(data => console.log(data));
  //     alert('Product Created!')
  //     history.push('/')
  //   }

  // React.useEffect(() => {
  //   fetch('/return-certs')
  //     .then(response => response.json())
  //     .then(data => setCerts(data));
  //     },[]);

  // const [dataobjectlist, setdataobjectlist] = React.useState([{}]);

// for object in dataobjectlist:
// return (
//   <div> {object.attr}<div>
// )

function CreateMealPlan() { 
  //take in search form data, send to server to create mealplans,
  // receive back mealplan ids, history.push to /mealplans *indicate new ones

  const [ingredients, setIngredients] = React.useState(''); 
  const [num_recipes_day, setNumRecipes] = React.useState('');
  const [start_date, setStartDate] = React.useState('');
  const [end_date, setEndDate] = React.useState('');
  const [mealplan_list, setMealPlanList] = React.useState([]);
  const history = useHistory()

  function handleCreate(evt) {
    evt.preventDefault();

    const data = { 
      ingredients: ingredients,
      num_recipes_day: num_recipes_day,
      start_date: start_date, // string, needs to be converted to datetime obj
      end_date: end_date  // string, needs to be converted to datetime obj
    }
    
    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

      fetch('/api/create', options)
      .then(response => response.json())
      .then(data => {
        history.push('/mealplans')
        setMealPlanList(data)});
  }

  function handleIngredients(evt) {
    setIngredients(evt.target.value)
  }

  function handleClick(evt) {  
    setNumRecipes(evt.target.value)
  }

  function handleStartDate(evt) {
    // convert start_date string to a better format
    setStartDate(evt.target.value)
  }

  function handleEndDate(evt) {

    setEndDate(evt.target.value)
  }

  // function handleClick(id) {
  //   history.push({pathname:`/mealplan/${mp.id}`});
  // };

  return (
    <React.Fragment>
      <form onSubmit={handleCreate}>
        Ingredients:
        <input value={ingredients} onChange={handleIngredients} type="text"></input>
        Number of Recipes:
        <div>
          <input type="radio" name="recipes_per_day" value="1" onClick={handleClick}/> 1
          <input type="radio" name="recipes_per_day" value="2" onClick={handleClick}/> 2
          <input type="radio" name="recipes_per_day" value="3" onClick={handleClick}/> 3
          <input type="radio" name="recipes_per_day" value="4" onClick={handleClick}/> 4
          <input type="radio" name="recipes_per_day" value="5" onClick={handleClick}/> 5
        </div>
        Start Date:
        <input value={start_date} onChange={handleStartDate} type="date"></input>
        End Date:
        <input value={end_date} onChange={handleEndDate} type="date"></input>
        <button> Search </button>
      </form>
  </React.Fragment>
    )}

function Mealplans() {
  const[mealplans, setMealplans] = React.useState([])

  React.useEffect(() => {
    fetch("api/mealplans")
    .then(response => response.json())
    .then(data => setMealplans(data));
    }, []);

  return (
    <ul>
      {mealplans.map((mp) => {
        return (
          <li> 
            <Link to={`/mealplan/${mp.id}`}> Mealplan for {mp.date} </Link>
          </li>
        )
      })}
    </ul>
  )
  
}

function Mealplan() {
  let {mealplan_id} = useParams()

  const [mealplan, setMealplan] = React.useState({'recipes': [], 'altrecipes': []})
  let recipe_ids 
  let altrecipe_ids

  if (mealplan['recipes']) {
    recipe_ids = mealplan['recipes'].map((recipe) => {recipe['id']})
  }
  
  if (mealplan['altrecipes']) {
    altrecipe_ids = mealplan['altrecipes'].map((recipe) => {recipe['id']})
  }
  //test to make sure cal events are the updated recipes (udpated state)

  console.log(recipe_ids)
  console.log(altrecipe_ids)
  
  React.useEffect(() => (
    fetch(`/api/mealplan/${mealplan_id}`)
    .then(response => response.json())
    .then(data => setMealplan(data))
  ), [])

  function handleClick() {

    const data = { 
      mealplan_id: mealplan_id,
      recipe_ids: recipe_ids,
      altrecipe_ids: altrecipe_ids,
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    fetch('/api/cal', options)
    .then(response => response.json())
    .then(data => {
      if (data === 'Recipes added to MealPlan calendar!') {
        alert(data);
        history.push('/mealplans');
      } else { 
        alert("error");
      }
    })

   return ("added to calendar")  // can handle click return a button tha
  };

  function moveToRec(alt_recipe_id) {
    const new_mealplan = {'recipes':[{}], 'altrecipes' :[{}]}
    let recipe_to_move = {}
    for (const recipe of mealplan['altrecipes']) {
      console.log("recipe", recipe)
      if (recipe['id'] === alt_recipe_id) {
        recipe_to_move = recipe
        console.log("recipe to move", recipe_to_move)
      }
    }
    new_mealplan['recipes'] = mealplan['recipes'].concat([recipe_to_move])
    new_mealplan['altrecipes'] = mealplan['altrecipes'].filter(mp => mp['id'] !== alt_recipe_id)
    setMealplan(new_mealplan)
  }

  function moveToAlt(recipe_id) {
    const new_mealplan = {'recipes':[{}], 'altrecipes' :[{}]}
    let recipe_to_move = {}
    for (const recipe of mealplan['recipes']) {
      if (recipe['id'] === recipe_id) {
        recipe_to_move = recipe
        console.log("recipe to move", recipe_to_move)
      }
    }
    new_mealplan['altrecipes'] = mealplan['altrecipes'].concat([recipe_to_move])
    new_mealplan['recipes'] = mealplan['recipes'].filter(mp => mp['id'] !== recipe_id)
    setMealplan(new_mealplan)
  }

  return (
    <React.Fragment>
      <h3> Mealplan {mealplan_id} </h3>
      <td> Please select one of these recipes to REMOVE:
        {mealplan['recipes'].map((recipe) => {
          return (
            <React.Fragment>
              <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']}/>
              <button onClick={() => moveToAlt(recipe['id'])} name="remove" value="{recipe['id']}"> Remove </button>
            </React.Fragment>
            )
          })
        }
      </td>

      <td> Please select one of these recipes to ADD:
        {mealplan['altrecipes'].map((alt_recipe) => {
          return (
            <React.Fragment>
              <Recipe name={alt_recipe['name']} image={alt_recipe['image']} cook_time={alt_recipe['cook_time']} url={alt_recipe['url']} />
              <button onClick={() => moveToRec(alt_recipe['id'])} name="add" value="{alt_recipe['id']}"> Add </button>
          </React.Fragment>
            )
          })
        }
      </td>
      Looks good <button onClick={handleClick}> Add to Calendar </button>
    </React.Fragment>  
)
}


function Recipe(props) {
  return (
    <tr>
      {props.name}<br></br>
      Cook time: {props.cook_time}<br></br>
      <a href={props.url} > Click to go to recipe </a><br></br>
      <img src={props.image} variant="left" width="150" height="150"></img><br></br>
    </tr>
  )
}


function Recipes() {

  const[recipes, setRecipes] = React.useState([])

  React.useEffect(() => (
    fetch("api/recipes")
    .then(response => response.json())
    .then(data => {
      setRecipes(data) 
    })
  ), [])  

  return (
    <td>
      {recipes.map((recipe) => {
        return (
          <tr> 
            <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']} />
          </tr>
        )
      })}
    </td>
  )
}


function App() {
    return (
      <Router>
        <nav>
          <ul>
            <li>
                <Link to="/"> Home </Link>
            </li>
            <li>
                <Link to="/login"> Login </Link>
            </li>
            <li>
                <Link to="/recipes"> Recipes </Link>
            </li>
            <li>
                <Link to="/create_mealplan"> Create a Mealplan </Link>
            </li>
            <li>
                <Link to="/mealplans"> View My Mealplans </Link>
            </li>
          </ul>
        </nav>
        <div>
          <Switch>
            <Route path="/login">
              <LogIn />
            </Route>
            <Route path="/recipes">
              <Recipes />
            </Route>
            <Route path="/create_mealplan">
              <CreateMealPlan />
            </Route>
            <Route path="/mealplan/:mealplan_id">
              <Mealplan />
            </Route>
            <Route path="/mealplans">
              <Mealplans />
            </Route>
            <Route path="/">
              <Homepage />
            </Route>
          </Switch>
        </div>
      </Router>
    );
  }

ReactDOM.render(<App />, document.getElementById('root'))
