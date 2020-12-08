function Homepage(props) {
  const history = useHistory()

  function handleClick(evt) {
    evt.preventDefault
    history.push('/create');
  }

  return (
    <React.Fragment>
      <div className="bg-salt bg flex-container-center"> 
        <div className="flex-item-welcome welcome-font wood-text"> Welcome {props.user.name} </div>
        <div className="flex-item-welcome2"> 
          <Button href="/create_mealplan" onClick={handleClick} variant="outline-primary" size="lg"> Get Started </Button>
        </div>
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
      <div className="bg-salt bg flex-container-center">
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
        <Button id="center" variant="outline-primary" type="submit"> Log In </Button>
        </Form>
        Authorize with Google
          <a className="btn btn-primary" type="submit" href="/authorize" role="button"> Authorize</a>
      </div>
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
      <div className="bg-salt bg flex-container-center">
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
          <Button id="center" variant="outline-primary" type="submit"> Create Account </Button>
        </Form>
      </div>
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
        <div className="form-background">
          <div className="flex-item-search create-form-font">
            <Form onSubmit={handleCreate} >
              <Form.Group id="search-input-font">
                <Form.Label>Ingredients:</Form.Label>
                <Form.Control type="text" value={ingredients} id="search-input-font" placeholder="enter ingredients here" onChange={handleIngredients}></Form.Control>
              </Form.Group>
            <br></br>
            <Form.Group controlId="exampleForm.ControlSelect1">
              <Form.Label>Recipes per day:</Form.Label>
              <Form.Control onChange={handleChange} value={num_recipes_day} as="select">
                  <option selected>Select Number</option>
                  <option name="recipes_per_day" value="1">1</option>
                  <option name="recipes_per_day" value="2">2</option>
                  <option name="recipes_per_day" value="3">3</option>
                  <option name="recipes_per_day" value="4">4</option>
                  <option name="recipes_per_day" value="5">5</option>
              </Form.Control>
            </Form.Group>
            <br></br>
            <Form.Group>
              <Form.Label>Dates:</Form.Label><br></br>
                <DatePicker className="lightpicker" setPicker={setPicker}/>
            </Form.Group>
            <br></br>
            <br></br>
            <div id="create-button">
            <Button type="submit">Create</Button>
            </div>
            </Form>
          </div>
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
      <div className="parallax-salt">
        <div className="flex-container-wrap">
          {mealplans.map((mp) => {
            return (
              <div className="flex-item-mp">
                <div className="flex-container-stuck">
                  <div className="flex-item-mp-icon">
                    <div className="flex-container-i">
                      <a href={`/mealplan/${mp.id}`}>
                        <span class="fa-stack fa-2x">
                          <i class="fas fa-circle fa-stack-2x fa-inverse fa-xs"></i>
                          <i class="fas fa-utensils fa-stack-1x fa-xs"></i>
                        </span>
                      </a>
                    </div>
                  </div>
                  <div className="flex-item-mp">
                    <br></br><p id="mp-font"> MEALPLAN FOR </p>
                    <a className="justify" id="mp-link-font"> {mp.date} </a>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </React.Fragment>
  )
}


function Mealplan() {
  let {mealplan_id} = useParams()

  const [mealplan, setMealplan] = React.useState({'recipes': [], 'altrecipes': []})

  let recipe_ids = mealplan['recipes'].map(recipe => recipe['id']);
  let altrecipe_ids = mealplan['altrecipes'].map(recipe => recipe['id']);
  const mealplan_date = mealplan['date']
  
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
      <div className="parallax-meals">
      <h2 id="h2-font-size"> Mealplan {mealplan_id} </h2>
        <p id="mp-date-font-size"> {mealplan_date} </p>
        <div className="flex-container-divider">
          <div className="flex-item-divider">
          <p id="mp-font-size">Select recipe(s) to REMOVE:</p>
          </div>
        </div>
        <div className="flex-container-mp">
          {mealplan['recipes'].map((recipe) => {
            return (
              <div className="flex-item-mp-recipes">
                  <Recipe onClick={() => moveToAlt(recipe['id'])} buttonName="Remove" value="{recipe['id']}" name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']}/>
              </div>
              )
            })
          }
        </div>
        <div className="flex-container-divider">
          <div className="flex-item-divider">
            <p id="mp-font-size">Select recipe(s) to ADD:</p>
          </div>
        </div>
        <div className="flex-container-mp">
          {mealplan['altrecipes'].map((alt_recipe) => {
            return (
              <div className="flex-item-mp-recipes">
                  <Recipe onClick={() => moveToRec(alt_recipe['id'])} buttonName="Add" value="{alt_recipe['id']}" name={alt_recipe['name']} image={alt_recipe['image']} cook_time={alt_recipe['cook_time']} url={alt_recipe['url']} />
              </div>
              )
            })
          }
        </div>
        <div>
          <div className="flex-item-button">
            <button type="button" className="btn btn-primary" onClick={handleClick}>Add to Calendar</button>
          </div>
        </div>
      </div>
    </React.Fragment>  
)
}


function Recipe(props) {

  return (
    <Card border="info" style={{ width: '16.5rem' }} className="card">
      <Card.Img top width="100%" variant="top" src={props.image} className="card-img" alt="Card image cap" />
      <Card.Body>
        <Card.Title>{props.name} </Card.Title>
        <Card.Text>
          Cook time: {props.cook_time} minutes
        </Card.Text>
        <Button className="button-border" variant="info" href={props.url}>Go to Recipe</Button>
        {props.buttonName? <Button className="button-border absolute" onClick={props.onClick} variant="info" href={props.url}>{props.buttonName}</Button>: " "}
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

  return (
    <React.Fragment>
      <div className="parallax-salt">
        <div className="recipe-container-divider"> 
        <p className="recipe-font wood-text"> Recipes </p>
        </div>
        <div className="flex-container-recipes"> 
          {recipes.map((recipe) => {
            return (
              <div className="flex-item-mp-recipes">
                <Recipe name={recipe['name']} image={recipe['image']} cook_time={recipe['cook_time']} url={recipe['url']} />
              </div>
            )
          })}
        </div>
      </div>
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
      <Navbar bg="light" expand="lg" className="navbar-color navbar-background-color">
        <Navbar.Brand className="nav-link navbar-color navbar-brand:hover navbar-brand:focus" href="/"> 
          <div className="navbar-brand">
            <span id="gray">carda</span>
            <span id="purple">mom</span>
          </div>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            {user.id ? '' : <Nav.Link href="/login"> Login </Nav.Link>}
            {user.id ? '' : <Nav.Link href="/new_user"> Create Account</Nav.Link>}
            <Nav.Link href="/recipes"> Recipes </Nav.Link>
            {user.id ? <Nav.Link href="/create_mealplan"> Create a Mealplan </Nav.Link> : ''}
            {user.id ? <Nav.Link href="/mealplans"> View My Mealplans </Nav.Link> : ''}
          </Nav>
          <Nav.Item className="ml-auto">
            {user.id ? <Button href="/" onClick={logOut} variant="outline-secondary"> Log Out </Button> : ''}
          </Nav.Item>
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
