import { useState } from 'react'
import './App.css'
import { IEvent } from './interfaces/IEvent'
import { EventsList } from './components/EventsList'


function App() {
  const [events, setEvents] = useState<IEvent[]>([])
  const [selectedEvents, setSelectedEvents] = useState<IEvent[]>([])
  const [calendarUri, setCalendarUri] = useState("")
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  async function create_calendar() {
    const response = await fetch("http://localhost:8000/calendar/", {
      method:"POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(selectedEvents)
    })
    const data = await response.json()
    setCalendarUri(data.link)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setCalendarUri("")
      setEvents([])
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        setError(false)
        setLoading(true)
        const response = await fetch("http://localhost:8000/ai/pdf_events/", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setEvents(data)
          setLoading(false)
          setError(false)
        }
      } catch (error) {
        setError(true)
      }
      setLoading(false)
    }
  };


  const handleSelectedEventsChange = (events: IEvent[]) => {
    setSelectedEvents(events)
  }

  return (
    <div style={{display: "flex", flexDirection:"column", alignItems:"center"}}>
      <h1>Calendarizador Programas UC</h1>
      <h2>Crea tu calendario en 3 simples pasos!</h2>
      <div style={{maxWidth:"23em"}}>
        <ol>
          <li>Sube un archivo .pdf con el programa de tu curso</li>
          <li>Revisa y selecciona que las fechas entregadas por el programa son correctas</li>
          <li>Genera y descarga el archivo generado (.ics) agregalo a tu calendario!</li>
        </ol>
      </div>
          
      
      <div style={{display: 'flex', flexDirection: "column", alignItems: "center", rowGap: "1em"}}>
        <input type="file" onChange={handleFileChange} />
        {file && 
          loading ? 
          <button disabled>Cargando Eventos...</button> :
          <button onClick={handleUpload}>{error ? "Intentalo Denuevo" : "Obtener Fechas"}</button>
        }
      </div>
      <div style={{padding: "1em"}}>
        <EventsList events={events} handleSelectedEventsChange={handleSelectedEventsChange}></EventsList>
      </div>
      <div style={{display: "flex", flexDirection: "column", alignItems:"center"}}>
        {calendarUri === ""? 
          (events.length !== 0 && (<button style={{width: "12em"}} onClick={create_calendar}>Crear Calendario</button>)):
          (<a href={calendarUri} className='button'>Descargar Calendario</a>)
        }
      </div>
      <div style={{maxWidth:"23em"}}>
        <p>* Si no logras cargar el archivo en tu calendario acá hay instrucciones específicas para <a href="https://support.google.com/calendar/answer/37118?hl=es-419&co=GENIE.Platform%3DDesktop" target='_blank'>Google Calendar</a> o <a href="https://support.microsoft.com/en-us/office/import-calendars-into-outlook-8e8364e1-400e-4c0f-a573-fe76b5a2d379" target='_blank'>Outlook</a></p>
      </div>
    </div>
  )
}

export default App
