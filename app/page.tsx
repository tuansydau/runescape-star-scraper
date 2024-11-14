"use client";

import { useEffect, useState, Fragment } from "react";

export default function Home() {
  const [stars, setStars] = useState([]);

  useEffect(() => {
    const fetchStars = async () => {
      const response = await fetch("http://localhost:8080/api/scrape");
      const jsonData = await response.json();
      setStars(jsonData);
    };
    fetchStars();
  }, []);

  return (
    <>
      <div className="text-white">
        {stars.length !== 0
          ? stars.map((star, index) => (
              <Fragment key={index}>
                {star[0]} {star[1]} {star[2]} {star[3]}
                <br />
              </Fragment>
            ))
          : "Loading..."}
      </div>
    </>
  );
}
