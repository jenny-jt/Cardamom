function Homepage(props) {
  return (
    <React.Fragment>
      <div className="bg-salt bg flex-container-center"> 
        <div className="flex-item-welcome"> Welcome {props.user.name} </div>
      </div>
    </React.Fragment>
  ) 
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
        history.push('/');
      } else {
        alert("Email and/or password not valid. If you have an account, please try logging in again")
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
      <Container>
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
      </Container>
    </React.Fragment>
  ) 
}


function CreateUser(props) {
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
  const [mealplan_list, setMealPlanList] = React.useState([]);
  const [picker, setPicker] = React.useState(); 
  const history = useHistory()

  function handleCreate(evt) {
    evt.preventDefault();

    const start_date = picker.getStartDate().toISOString()
    console.log(start_date)
    const end_date = picker.getEndDate().toISOString()
    console.log(end_date)

    const data = {
      ingredients: ingredients,
      num_recipes_day: num_recipes_day,
      start_date: start_date,
      end_date: end_date,
      user_id: props.user.id
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

  return (
    <React.Fragment>
      <div className="bg-seasoning bg flex-container-center">
        <div className="flex-item-search">
          <Form onSubmit={handleCreate} >
            <Form.Group>
              <Form.Label>Ingredients:</Form.Label>
              <Form.Control type="text" value={ingredients} placeholder="enter ingredients here" onChange={handleIngredients}></Form.Control>
            </Form.Group>

          <Form.Group controlId="exampleForm.ControlSelect1">
            <Form.Label>Number of Recipes per day:</Form.Label>
            <Form.Control onChange={handleChange} value={num_recipes_day} as="select">
                <option selected>Select Number</option>
                <option name="recipes_per_day" value="1">1</option>
                <option name="recipes_per_day" value="2">2</option>
                <option name="recipes_per_day" value="3">3</option>
                <option name="recipes_per_day" value="4">4</option>
                <option name="recipes_per_day" value="5">5</option>
            </Form.Control>
          </Form.Group>

          <Form.Group>
            <Form.Label>Dates you would like meal plans for:</Form.Label><br></br>
              <DatePicker setPicker={setPicker}/>
          </Form.Group>

          <Button type="submit">Create</Button>
          </Form>
        </div>
      </div> 
    </React.Fragment>
    )}


function DatePicker(props) {
  const dateRef = React.useRef(null);

  React.useEffect( () => {
    const dateSelect = new Litepicker({ 
      element: dateRef.current,
      singleMode: false,
      selectForward: false,
      startDate: null,
      endDate: null,
      numberOfMonths: 2,
      numberOfColumns: 2,
      format: 'YYYY-MM-DD'
    });
    props.setPicker(dateSelect)
  }, [])


  // callback ref -- when provided as a ref react will 
  // call this function whenever 
  // the ref gets attatched to a different node

  // the primary use for useCallback is simply to return a memoized callback
  // but it can be combined with ref in this way :) 
  // const refCallback = React.useCallback(node => {
  //   if (node !== null) {
  //     const dateSelect = new Litepicker({ 
  //       element: refCallback.current,
  //       singleMode: false,
  //       selectForward: false,
  //       startDate: null,
  //       endDate: null,
  //       numberOfMonths: 2,
  //       numberOfColumns: 2,
  //       format: 'YYYY-MM-DD'
  //     });
  //   }
  // }, [])

  return (
    <input ref={dateRef} id="dateSelect"/>
  )
}


function Mealplans(props) {
  console.log("mealplans being rendered", props.user)
  const[mealplans, setMealplans] = React.useState([])
  const data = {"user_id": props.user.id}
  console.log("data in Mealplans which contains user id", data)

  React.useEffect(() => {

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    if (props.user.id) {
      fetch("api/mealplans", options)
      .then(response => response.json())
      .then(data => setMealplans(data));
    }
  }, [props.user.id]);

  return (
    <React.Fragment>
      <div className = "bg-salt bg flex-container-center">
      {mealplans.map((mp) => {
        return (
          <div className="flex-item-search">
            <ListGroup variant="flush">
              <ListGroup.Item action href={`/mealplan/${mp.id}`}> Mealplan for {mp.date} </ListGroup.Item>
            </ListGroup>
          </div>
        )
      })}
      </div>
    </React.Fragment>
  )
}


function Mealplan() {
  let {mealplan_id} = useParams()

  const [mealplan, setMealplan] = React.useState({'recipes': [], 'altrecipes': []})

  let recipe_ids = mealplan['recipes'].map(recipe => recipe['id']);
  let altrecipe_ids = mealplan['altrecipes'].map(recipe => recipe['id']);
  
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
    console.log("data", data)

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
        console.log("new recipe to move", recipe_to_move)
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
        console.log("old recipe to move", recipe_to_move)
      }
    }
    new_mealplan['altrecipes'] = mealplan['altrecipes'].concat([recipe_to_move])
    new_mealplan['recipes'] = mealplan['recipes'].filter(mp => mp['id'] !== recipe_id)
    setMealplan(new_mealplan)
  }

  return (
    <React.Fragment>
      <Container fluid={true}>
      <h3> Mealplan {mealplan_id} </h3>
        Please select one of these recipes to REMOVE:
        <ListGroup horizontal>
          {mealplan['recipes'].map((recipe) => {
            return (
              <ListGroup.Item action variant="info">
                <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']}/>
                <button onClick={() => moveToAlt(recipe['id'])} name="remove" value="{recipe['id']}" type="button" className="btn btn-outline-secondary btn-sm active" role="button" aria-pressed="true"> Remove </button>
              </ListGroup.Item>
              )
            })
          }
        </ListGroup>
      </Container>

      <Container fluid={true}>
        Please select one of these recipes to ADD:
        <ListGroup horizontal>
          {mealplan['altrecipes'].map((alt_recipe) => {
            return (
              <ListGroup.Item action variant="warning">
                <Recipe name={alt_recipe['name']} image={alt_recipe['image']} cook_time={alt_recipe['cook_time']} url={alt_recipe['url']} />
                <Card.Footer>
                  <small className="text-muted">Last updated 3 mins ago</small>
                </Card.Footer>
                <button onClick={() => moveToRec(alt_recipe['id'])} name="add" value="{alt_recipe['id']}" type="button" className="btn btn-outline-warning btn-sm active" role="button" aria-pressed="true"> Add </button>
              </ListGroup.Item>
              )
            })
          }
      </ListGroup>
      </Container>
      Looks good <button type="button" className="btn btn-primary" onClick={handleClick}>Add to Calendar</button>
    </React.Fragment>  
)
}


function Recipe(props) {

  return (
    <Card border="info" style={{ width: '18rem' }} className="card">
      <Card.Img top width="100%" variant="top" src={props.image} className="card-img" alt="Card image cap" />
      <Card.Body>
        <Card.Title>{props.name} </Card.Title>
        <Card.Text>
          Cook time: {props.cook_time} minutes
        </Card.Text>
        <Button variant="info" href={props.url}>Go to Recipe</Button>
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
    const recipeColumn = recipes.map((recipe) => {
      return (
        <Col xs={6} md={4}>
          <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']} />
        </Col>
      )
    })

    let rows = []

    for (let i =0; i < recipeColumn.length; i+=3) {
      rows.push(
        <Row> {recipeColumn[i]} {recipeColumn[i+1]} {recipeColumn[i+2]} </Row>
      )
    }
    return rows
  }

  return (
    <React.Fragment>
      <Container className="page-container">
        {generateRecipes()}
      </Container>
    </React.Fragment>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <span className="text-muted">Footer</span>
      </div>
  </footer>
  )
}


function App() {
  const [user, setUser] = React.useState({}) //USER LOCALLY DEFINED

  React.useEffect(() => {
    const user_in_storage = localStorage.getItem('user')
    if (user_in_storage) {
      setUser(JSON.parse(user_in_storage));
    }
  },[]);

  console.log("user in storage", user);
  console.log("user id", user.id)

  function logOut() {
    setUser({});
    localStorage.clear();
    return(alert('logged out'))
  }

  return (
    <Router>
      <Navbar bg="light" expand="lg" className="navbar-color">
        <Navbar.Brand href="/">Meal Planner</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            {user.id ? '' : <Nav.Link href="/login"> Login </Nav.Link>}
            {user.id ? '' : <Nav.Link href="/new_user"> Create Account</Nav.Link>}
            <Nav.Link href="/recipes"> Recipes </Nav.Link>
            {user.id ? <Nav.Link href="/create_mealplan"> Create a Mealplan </Nav.Link> : ''}
            {user.id ? <Nav.Link href="/mealplans"> View My Mealplans </Nav.Link> : ''}
            {user.id ? <Button href="/" onClick={logOut} variant="outline-primary"> Log Out </Button> : ''}
          </Nav>
          {/* <Form inline>
            <FormControl type="text" placeholder="Email" className="mr-sm-2" />
            <Button variant="outline-success">Log In</Button>
          </Form> */}
        </Navbar.Collapse>
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
