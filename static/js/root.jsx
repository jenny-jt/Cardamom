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
const Col = ReactBootstrap.Col;
const Card = ReactBootstrap.Card;
const CardDeck = ReactBootstrap.CardDeck;
const CardColumns = ReactBootstrap.CardColumns;
const CardBody = ReactBootstrap.CardBody;
const CardImage = ReactBootstrap.CardImage;
const CardTitle = ReactBootstrap.CardTitle;
const CardText = ReactBootstrap.CardText;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;


function Homepage(props) {
  return <div> Welcome {props.user.name} </div>
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

    fetch('/api/login', options) 
    .then(response => response.json())
    .then(data => {
      console.log("fetch is running", data);
      if (data !== 'no user with this email') {
        props.setUser(data);
        localStorage.setItem('user', JSON.stringify(data));
        console.log("user after setItem", props.user)
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


function CreateUser() {
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const history = useHistory()

  function handleNewUser(evt) {
    evt.preventDefault();

    const data = { 
      name: name,
      email: email,
      password: password
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {'Content-Type': 'application/json'}
    }

    fetch('/api/new_user', options) 
    .then(response => response.json())
    .then(data => {
      console.log("new user data", data);
      if (data !== 'user with this email already exists') {
        props.setUser(data);
        localStorage.setItem('user', JSON.stringify(data));
        history.push('/');
      } else {
        alert("user with this email already exists")
      }
      });
  }

  function handleNameChange(evt) {
    setName(evt.target.value)
  }
  function handleEmailChange(evt) {
    setEmail(evt.target.value)
  }

  function handlePasswordChange(evt) {
    setPassword(evt.target.value)
  }

  return (
    <React.Fragment>
      <Form onSubmit={handleNewUser}>
      <Form.Group>
        <Form.Label>Name</Form.Label>
        <Form.Control type="text" value={name} onChange={handleNameChange} placeholder="Name" />
      </Form.Group>
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
    </React.Fragment>
  ) 
}


function CreateMealPlan(props) { 
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
        setMealPlanList(data);
        history.push('/mealplans');
        });
  }

  function handleIngredients(evt) {
    setIngredients(evt.target.value)
  }

  function handleChange(evt) {  
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
          <Form.Control type="text" value={ingredients} placeholder="enter ingredients here" onChange={handleIngredients}></Form.Control>
        </Form.Group>

        <Form.Group controlId="exampleForm.ControlSelect1">
        <Form.Label>Number of Recipes:</Form.Label>
        <Form.Control onChange={handleChange} value={num_recipes_day} as="select">
            <option name="recipes_per_day" value="1" defaultValue>1</option>
            <option name="recipes_per_day" value="2">2</option>
            <option name="recipes_per_day" value="3">3</option>
            <option name="recipes_per_day" value="4">4</option>
            <option name="recipes_per_day" value="5">5</option>
        </Form.Control>
        </Form.Group>
{/* 
      <Form>
        {['checkbox'].map((type) => (
          <div key={`inline-${type}`} className="mb-3">
            <Form.Check inline label="1" type={type} checked={num_recipes_day} onClick={handleChange} id={`inline-${type}-1`} />
            <Form.Check inline label="2" type={type} checked={num_recipes_day} onClick={handleChange} id={`inline-${type}-2`} />
            <Form.Check inline label="3" type={type} checked={num_recipes_day} onClick={handleChange} id={`inline-${type}-3`} />
            <Form.Check inline label="4" type={type} checked={num_recipes_day} onClick={handleChange} id={`inline-${type}-4`} />
            <Form.Check inline label="5" type={type} checked={num_recipes_day} onClick={handleChange} id={`inline-${type}-5`} />
          </div>
        ))}
      </Form> */}

      <Form.Group>
        <Form.Label>Start Date:</Form.Label>
        <Form.Control type="date" value={start_date} onChange={handleStartDate} type="date"/>
        <Form.Label>End Date:</Form.Label>
        <Form.Control type="date" value={end_date} onChange={handleEndDate} type="date"/>
      </Form.Group>
        <Button type="submit">Create</Button>
      </Form>
    </React.Fragment>
    )}


function Mealplans(props) {
  const[mealplans, setMealplans] = React.useState([])

  React.useEffect(() => {
    const data = {'user_id': props.user.id}
    console.log("data in Mealplans", data)

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
          <ListGroup>
          <ListGroup.label> Mealplan for {mp.date} </ListGroup.label>
          <ListGroup.Item action href={`/mealplan/${mp.id}`}> </ListGroup.Item>
          </ListGroup>
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
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
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
    <Card border="secondary" style={{ width: '18rem' }}>
      <Card.Img top width="100%" variant="top" src={props.image} alt="Card image cap" />
      <Card.Body>
        <Card.Title>{props.name} </Card.Title>
        <Card.Text>
          Cook time: {props.cook_time} minutes
        </Card.Text>
        <Button variant="primary" href={props.url}>Go to Recipe</Button>
      </Card.Body>
    </Card>
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

  function generateRecipes() {
    const recipe_column = recipes.map((recipe) => {
      return (
        <Col xs={6} md={4}>
          <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']} />
        </Col>
      )
    })

    let rows = []

    for (let i =0; i < recipe_column.length; i+=3) {
      let row_recipes = <row> {recipe_column[i]} {recipe_column[i+1]} {recipe_column[i+2]} </row>
      console.log(row_recipes)
      rows.push(row_recipes);
         
    return rows
    }}

  return (
    <React.Fragment>
      {generateRecipes()}
    </React.Fragment>
  )
}


function App() {
  const [user, setUser] = React.useState({}) //USER LOCALLY DEFINED

  React.useEffect(() => {
    const user_in_storage = localStorage.getItem('user')
    if (user_in_storage) {
      setUser(JSON.parse(user_in_storage))
    }
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
            <CreateMealPlan user={user}/>
          </Route>
          <Route path="/mealplan/:mealplan_id">
            <Mealplan />
          </Route>
          <Route path="/mealplans">
            <Mealplans user={user}/>
          </Route>
          <Route path="/new_user">
            <CreateUser user={user} setUser={setUser}/>
          </Route>
          <Route path="/">
            <Homepage user={user}/>
          </Route>
        </Switch>
      </Router>
    );
  }

ReactDOM.render(<App />, document.getElementById('root'))
