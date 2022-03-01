import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';

function Solveproblem() {
    const navigate = useNavigate()
    const {id} = useParams()
    const [showdesc,setShowdesc] = useState(true)
    const [showsol,setShowsol] = useState()
    const [problemdata,setProblemdata] = useState({})


    const toShow = (to)=>{
        // console.log(to)
        switch(to){
            case "desc":{
                setShowdesc(true)
                setShowsol(false)
                break
            }
            case "sol":{
                setShowdesc(false)
                setShowsol(true)
            }
        }
    }
    useEffect(()=>{
        axios.get(`http://127.0.0.1:8000/user/getoneproblem/${id}`).then(res => {
            if (!res.data.islogin) {
                navigate('/')
            }
            setProblemdata(res.data.data)
            console.log(res.data.data)
        })
    },[])
  return (
    <div className='solvingcont'>
    
        <div className="aboutproblem">
            <div className="probleminfo">
                <div className={showdesc?"active":""} onClick={()=>toShow("desc")}>Description</div>
                <div className={showsol?"active":""} onClick={()=>toShow("sol")}>Solution</div>
            </div>
            <div className="view">
                {showdesc?<div className="desc">{problemdata.description}</div>:""}
                {showsol?<div className="sol">{problemdata.solution?problemdata.solution:"Solution No Available"}</div>:""}
            </div>
            
        </div>
        <div className="solveproblem">

        </div>

    </div>
  )
}

export default Solveproblem