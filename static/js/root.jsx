const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;
const useParams = ReactRouterDOM.useParams;
const useHistory = ReactRouterDOM.useHistory;
const Navbar = ReactBootstrap.Navbar;
const Nav = ReactBootstrap.Nav;
const Form = ReactBootstrap.Form;
const Button = ReactBootstrap.Button;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;


function Homepage() {
  return <div> Welcome to my site </div>
}

function LogIn(props) { 

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const history = useHistory()

  function handleLogin(evt) {
    evt.preventDefault();

    const data = { 
      email: email,
      password: password
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {'Content-Type': 'application/json'}
    }

    fetch('/api/login', options) // THIS ROUTE IS RETURNING YOUR USER INFO BEING SET TO STORAGE
    .then(response => response.json())
    .then(data => {
      console.log("fetch is running", data);
      if (data !== 'no user with this email') {
        props.setUser(data);
        localStorage.setItem('user', JSON.stringify(data)); // THIS SETS USER TO STORAGE WITH INFO YOU GET FROM FETCH
        history.push('/');
      } else {
        alert("incorrect email/password")
      }
    });
  }


  function handleEmailChange(evt) {
    setEmail(evt.target.value)
  }

  function handlePasswordChange(evt) {
    setPassword(evt.target.value)
  }

  return (
    <React.Fragment>
      <Form onSubmit={handleLogin}>
        <Form.Group controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="text" value={email} onChange={handleEmailChange} placeholder="Enter email" />
        <Form.Text className="text-muted" >
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>
      <Form.Group controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" value={password} onChange={handlePasswordChange} placeholder="Password" />
      </Form.Group>
      <Button variant="primary" type="submit"> Log In </Button>
      </Form>
      Authorize with Google
        <a className="btn btn-primary" href="/authorize" role="button"> Authorize</a>
    </React.Fragment>
  ) 
}

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
      start_date: start_date, 
      end_date: end_date  
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
    setStartDate(evt.target.value)
  }

  function handleEndDate(evt) {
    setEndDate(evt.target.value)
  }

  return (
    <React.Fragment>
      <Form onSubmit={handleCreate}>
        <Form.Group>
          <Form.Label>Ingredients:</Form.Label>
          <input type="text" value={ingredients} placeholder={ingredients} onChange={handleIngredients}></input>
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlSelect1">
          <Form.Label>Number of Recipes:</Form.Label>
          <Form.Control as="select">
            <option name="recipes_per_day" value="1" onClick={handleClick}>1</option>
            <option name="recipes_per_day" value="2" onClick={handleClick}>2</option>
            <option name="recipes_per_day" value="3" onClick={handleClick}>3</option>
            <option name="recipes_per_day" value="4" onClick={handleClick}>4</option>
            <option name="recipes_per_day" value="5" onClick={handleClick}>5</option>
          </Form.Control>
        </Form.Group>
        <Form.Group>
          <Form.Label>Start Date:</Form.Label>
          <input value={start_date} onChange={handleStartDate} type="date"></input>
          <Form.Label>End Date:</Form.Label>
          <input value={end_date} onChange={handleEndDate} type="date"></input>
        </Form.Group>
        <Button type="submit">Create</Button>
      </Form>
    </React.Fragment>
    )}


function Mealplans(props) {
  const[mealplans, setMealplans] = React.useState([])

  React.useEffect(() => {
    const data = {'user_id': props.id}

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    fetch("api/mealplans", options)
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
    recipe_ids = mealplan['recipes'].map((recipe) => {recipe['id']});
  }
  
  if (mealplan['altrecipes']) {
    altrecipe_ids = mealplan['altrecipes'].map((recipe) => {recipe['id']});
  }
  //test to make sure cal events are the updated recipes (udpated state)

  console.log(recipe_ids)
  console.log(altrecipe_ids)
  
  React.useEffect(() => {
    fetch(`/api/mealplan/${mealplan_id}`)
    .then(response => response.json())
    .then(data => setMealplan(data));
    }, []);

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

   return ("added to calendar")  // can handle click return a button 
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
              <button onClick={() => moveToAlt(recipe['id'])} name="remove" value="{recipe['id']}" type="button" className="btn btn-outline-secondary btn-sm active" role="button" aria-pressed="true"> Remove </button>
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
              <button onClick={() => moveToRec(alt_recipe['id'])} name="add" value="{alt_recipe['id']}" type="button" className="btn btn-outline-warning btn-sm active" role="button" aria-pressed="true"> Add </button>
          </React.Fragment>
            )
          })
        }
      </td>
      Looks good <button type="button" className="btn btn-primary" onClick={handleClick}>Add to Calendar</button>
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
    <React.Fragment>
      <ul className="list-group">
      {recipes.map((recipe) => {
        return (
          <li className="list-group-item">
            <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']} />
          </li>
        )
      })}
      </ul>
    </React.Fragment>
  )
}


function App() {
  const [user, setUser] = React.useState({}) //USER LOCALLY DEFINED

  React.useEffect(() => {
    const currentuser = JSON.parse(localStorage.getItem('user'));
    setUser(currentuser)
  },[]);

  console.log(user);

    return (
      <Router>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="#home">Meal Planner</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav"/>
          {/* <Navbar.Collapse id="basic-navbar-nav"> */}
            <Nav className="mr-auto">
              <Nav.Link href="/"> Home </Nav.Link>
              <Nav.Link href="/login"> Login </Nav.Link>
              <Nav.Link href="/new_user"> Create Account</Nav.Link>
              <Nav.Link href="/recipes"> Recipes </Nav.Link>
              <Nav.Link href="/create_mealplan"> Create a Mealplan </Nav.Link>
              <Nav.Link href="/mealplans"> View My Mealplans </Nav.Link>
            </Nav>
            {/* <Form inline>
              <FormControl type="text" placeholder="Email" className="mr-sm-2" />
              <Button variant="outline-success">Log In</Button>
            </Form> */}
          {/* </Navbar.Collapse> */}
        </Navbar>

        <Switch>
          <Route path="/login">
            <LogIn user={user} setUser={setUser} />
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
            <Mealplans user={user}/>
          </Route>
          <Route path="/new_user">
            <CreateMealPlan />
          </Route>
          <Route path="/">
            <Homepage />
          </Route>
        </Switch>
      </Router>
    );
  }

ReactDOM.render(<App />, document.getElementById('root'))

                  {/* {props.user?       ''        :   <Nav.Link><Link to="/app/signup">Login | Signup</Link></Nav.Link>}
                        {props.user?
                        <NavDropdown title= {props.user.fname} id="basic-nav-dropdown">
                                <NavDropdown.Item><Link to="/app/user-profile">Profile</Link></NavDropdown.Item> */}
                                {/* {if user?  'do this' : 'else do this'} */}
