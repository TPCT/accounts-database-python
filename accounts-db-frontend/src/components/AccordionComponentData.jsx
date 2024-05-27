import React from "react";
import { transformKey } from "../utils/transformData";
import { IoIosArrowDown } from "react-icons/io";

const AccordionComponentData = ({ itemStatsData, slug, title }) => {
  const transformedData = Object.fromEntries(
    Object.entries(itemStatsData).map(([key, value]) => [
      transformKey(key),
      value,
    ])
  );
  return (
    <div className="accordion accordion-flush" id={`accordionFlush${slug}`}>
      <div className="accordion-item">
        <h2 className="accordion-header" id={`flush-heading${slug}`}>
          <button
            className="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target={`#flush-collapse${slug}`}
            aria-expanded="false"
            aria-controls={`flush-collapse${slug}`}
          >
            {title}
          </button>
        </h2>
        <div
          id={`flush-collapse${slug}`}
          className="accordion-collapse collapse"
          aria-labelledby={`flush-heading${slug}`}
          data-bs-parent={`#accordionFlush${slug}`} 
        >
          <div className="accordion-body">
            <div className="mb-3">
              <div className="row row-cols-1 row-cols-md-2">
                {Object.entries(transformedData).map(([key, value]) => (
                  <div key={key} className="col pt-3">
                    <label htmlFor={key} className="form-label  main-text-color">
                      {key}
                    </label>

                    <input
                      type="text"
                      className="form-control"
                      id={key}
                      value={key === 'Date Created' ? value.split('T')[0]:value}
                      disabled
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccordionComponentData;
