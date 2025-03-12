import React from 'react'
import { Link } from 'react-router-dom'

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="div-footer">
                <ul className="nav-list">
                    <li>
                        {' '}
                        <Link
                            to="/About"
                            className="navigation-link px-2 link-two"
                        >
                            About
                        </Link>
                    </li>
                </ul>
            </div>
        </footer>
    )
}

export default Footer
