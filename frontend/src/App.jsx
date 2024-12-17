import Select from 'react-select'
import logo from './assets/logo.jpg'
import { useState } from 'react'
import './App.css'

function App() {
  const [id, setId] = useState('')
  const [user, setUser] = useState('')
  const [data, setData] = useState({"helo": "Welcome to our app!"})
  const [selectOpen, setSelectOpen] = useState(false)
  const [phrases, setPhrases] = useState('')
  const [accessibleSections, setAccessibleSections] = useState({})
  const [showListHeader, setShowListHeader] = useState(false)

  const options = [
    { value: 1, label: "Hospital" },
    { value: 2, label: "Internal" }
  ];

  const onClick = async () => {
    if (id.length === 0) {
      setData({ 'helo': "please enter a patient ID" })
    } else if (user.length === 0) {
      setData({ 'helo': "please select a user role" })
    } else {
      let url = `http://localhost:5000/clinical_notes?user_role=${user}&patient_id=${id}`

      // Check if phrases input isn't empty
      if (phrases.trim().length > 0) {
        const parsedPhrases = phrases.split(', ')

        for (let i = 0; i < parsedPhrases.length; i++) {
          const phrase = parsedPhrases[i];
          url += `&required_header=${phrase}`
        }
      }

      //do the api call to get data
      const response = await fetch(url)

      if (response.ok) {
        const jsonResponse = await response.json()
        const {clinicalNotes, accesible_section} = jsonResponse
        setData({'helo': clinicalNotes})
        setAccessibleSections(accesible_section)
      } else {
        const errorResponse = await response.json()
        const errorMessage = errorResponse.error
        console.log(errorMessage)
        setData({'helo': errorMessage})
        setAccessibleSections({})
      }

      setShowListHeader(true)
    }
  }

  const toggleSelectIsOpen = () => {
    if (selectOpen) {
      setSelectOpen(false)
      document.querySelector('.Select_option input').blur();
    } else {
      setSelectOpen(true)
    }
  };

  return (
    <>
      <div className="App">
        <img src={logo} alt="Logo" className="logo"/>
        <input
            type="number"
            className="textbox"
            placeholder="Enter patient ID"
            value={id}
            onChange={(e) => {
              setId(e.target.value);
            }}
        />
        <input
            type="text"
            className="textbox"
            placeholder="Enter section keywords separated by ', '"
            value={phrases}
            onChange={(e) => {
              setPhrases(e.target.value);
            }}
        />
        <div className={`select-container ${selectOpen ? 'open' : ''}`}>
          <Select
              onChange={(selectedOption) => {
                setUser(selectedOption.value);
              }}
              options={options}
              className="Select_option"
              menuIsOpen={selectOpen}
              onMenuClose={toggleSelectIsOpen}
              onMenuOpen={toggleSelectIsOpen}
          />
        </div>
        <button onClick={onClick}>Search</button>
        <div className="columns">
          <p style={{whiteSpace: "pre-line"}}>
            {showListHeader && <b>Clinician Note For Patient</b>}
            <br/>
            {data.helo}
          </p>
          <p style={{whiteSpace: "pre-line"}}>
            {showListHeader && <b>Section Name: Accessible To User</b>}
            <br/>
            {Object.entries(accessibleSections).map(([key, value]) => (
                `${key} : ${value}`
            )).join("\n")}
          </p>
        </div>
      </div>
      </>
      )
      }

      export default App

