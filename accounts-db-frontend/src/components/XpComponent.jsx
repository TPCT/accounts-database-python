import React from "react";
import { IoIosArrowDown } from "react-icons/io";

const XpComponent = ({ xpData }) => {
  // "name": "avakinlife",
  // "level": 63,
  // "level_xp": 2720775,
  // "next_level": 64,
  // "next_level_xp": 2902675,
  // "leveled_up": 0

  return (
    <div className="accordion accordion-flush" id="accordionFlushExample">
      <div className="accordion-item">
        <h2 className="accordion-header" id="flush-headingOne">
          <button
            className="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#flush-collapseOne"
            aria-expanded="false"
            aria-controls="flush-collapseOne"
          >
            XP
          </button>
        </h2>
        <div
          id="flush-collapseOne"
          className="accordion-collapse collapse"
          aria-labelledby="flush-headingOne"
          data-bs-parent="#accordionFlushExample"
        >
          <div className="accordion-body">
            <div className="mb-3 row row-cols-1 row-cols-md-2">
              {xpData.map((xp) => {
                const totalXPRequired = xp.next_level_xp - xp.level_xp;
                const currentXpProgress = xp.xp - xp.level_xp;

                const progressPercentage =
                  Number(currentXpProgress / totalXPRequired) * 100;

                return (
                  <div className="col" key={xp.name}>
                    <div className="d-flex justify-content-center w-100">
                      <span
                          className="form-label main-text-color badge rounded-pill text-bg-primary"
                      >
                      {xp.name}
                    </span>
                    </div>
                    <label
                      htmlFor={xp.level}
                      className="form-label main-text-color my-4 pe-2"
                    >
                      Level:
                    </label>
                    <span className="badge rounded-pill secondary">
                      {xp.level}
                    </span>

                    <div className="">
                      <label className="form-label main-text-color">
                        Level Xp:
                      </label>
                      <div className="progress ">
                        <div
                          className="progress-bar"
                          role="progressbar"
                          style={{ width: progressPercentage + "%" }}
                          aria-valuenow={xp.level}
                          aria-valuemin="0"
                          aria-valuemax={totalXPRequired}
                        >
                          {progressPercentage.toFixed(0)}%
                        </div>
                      </div>
                    </div>

                    {/* <input
                    type="text"
                    value={xp.level_xp}
                    disabled
                    className="form-control"
                    id={xp.level_xp}
                  /> */}

                    <hr />
                  </div>
                  // <div key={item.name}>
                  //   {Object.entries(item).map(([key, value]) => (
                  //     <>
                  //       <label htmlFor="exampleFormControlInput1" className="form-label">
                  //         {key}
                  //       </label>
                  //       <input
                  //         type="email"
                  //         value={value}
                  //         className="form-control"
                  //         id="exampleFormControlInput1"
                  //         placeholder="name@example.com"
                  //       />
                  //     </>
                  //   ))}
                  // </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default XpComponent;
