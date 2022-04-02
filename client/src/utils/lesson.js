import * as d3 from "d3";

const classSize = 10;

function buildResponseMap(responseList) {
    const responseMap = {};
    responseList.forEach((response) => {
        responseMap[response.user_id] = response
    });
    return responseMap
}

class IdCounts {
    constructor() {
        this.counts = {}
    }
    increment(id) {
        if (this.counts[id] === undefined) {
            this.counts[id] = 1;
        } else {
            this.counts[id] += 1;
        }
    }
    decrement(id) {
        if (this.counts[id] !== undefined) {
            this.counts[id] -= 1;
        }
    }
}

class ResponseDataView {
    constructor(responseList, questionId) {
        this.responseMap = buildResponseMap(responseList)
        this.questionId = questionId;
    }

    updateResponse(response) {
        this.responseMap[response.user_id] = response;
        this.renderDetailedDisplay();
    }
}

class ParagraphResponseDataView extends ResponseDataView{
    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response paragraph')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${response.text}</span></div>`;
                }
            });
    }
}

class InlineTextResponseDataView extends ResponseDataView {
    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response inline-text')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${response.text}</span></div>`;
                }
            });
    }
}

class InlineSelectResponseDataView extends ResponseDataView {
    constructor(responseList, questionId, optionIdMap) {
        super(responseList, questionId);
        this.optionIdMap = optionIdMap;
    }

    renderDetailedDisplay() {
        const thisTracker = this;

        const $responseDisplay = $(`.apella-responses[questionId="${this.questionId}"]`);
        const $optionDisplay = $responseDisplay.find('.option-display');
        if ($optionDisplay.length === 0) {
            const selectableOptionsString = Object.values(this.optionIdMap).join(', ');
            $responseDisplay.prepend(`<div class='option-display'>Options: ${selectableOptionsString}</div>`)
        }

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response inline-select')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined || !response.selected_option_ids
                        || response.selected_option_ids.length === 0) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    let optionText = thisTracker.optionIdMap[response.selected_option_ids[0]];
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${optionText}</span></div>`;
                }
            });
    }
}

class ChoiceResponseDataView extends ResponseDataView {
    constructor(responseList, questionId, $questionElement) {
        super(responseList, questionId)

        this.optionIndicatorMap = {};
        $questionElement.find('.question-choice').each((i, node) => {
            this.optionIndicatorMap[$(node).attr('option-id')] = String.fromCharCode(i + 65);
        });

        this.#buildSummary();
    }

    #buildSummary() {
        this.selectedOptionCounts = new IdCounts();
        Object.values(this.responseMap).forEach((response) => {
            this.#addResponseToSummary(response);
        });
    }

    #addResponseToSummary(response) {
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.increment(selectedId));
    }

    #removeUserResponseFromSummary(userId) {
        const response = this.responseMap[userId];
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.decrement(selectedId));
    }

    renderSummary() {
        for (const [optionId, answeredCount] of Object.entries(this.selectedOptionCounts.counts)) {
            this.#renderChoiceOptionSummary(optionId, answeredCount);
        }
    }

    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response choice')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined || response.selected_option_ids.length === 0) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    let response_selections = ''
                    for (const optionId of response.selected_option_ids) {
                        response_selections += thisTracker.optionIndicatorMap[optionId];
                    }
                    return `<div class="name">${student.username}</div>
                            <div class="selection"><span>${response_selections}</span></div>`;
                }
            })
    }

    updateResponse(response) {
        if (this.responseMap[response.user_id] !== undefined) {
            this.#removeUserResponseFromSummary(response.user_id);
        }

        super.updateResponse(response);
        this.responseMap[response.user_id] = response;
        this.renderDetailedDisplay();

        this.#addResponseToSummary(response);
        this.renderSummary();
    }

    #renderChoiceOptionSummary(optionId, answered_count) {
        var myScale = d3.scaleLinear()
            .domain([0, classSize])
            .range([0, 100]);
        d3.selectAll(`.question-choice[option-id="${optionId}"] .response-chart`)
          .selectAll('rect')
          .data([answered_count])
          .join('rect')
            .transition()
          .attr('width', function(d) {
            return `${myScale(d)}%`;
          });
    }
}

class RubricResponseDataView extends ResponseDataView {
    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response paragraph')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${response.text}</span></div>`;
                }
            });
    }
}

const questionResponseTrackers = {};
const studentMap = {};

function toggleDetailedResponseDisplay(event) {
    const $targetElement = $(event.currentTarget);
    const questionId = $targetElement.attr('questionId');
    const questionType = $targetElement.attr('type')
    const responseTracker = questionResponseTrackers[questionId];
    let $expandedDisplay = $(`.apella-responses[questionId="${questionId}"]`)

    if (questionType === 'rubric') {
        let rubricItems = JSON.parse($targetElement.attr('items'));
        vueComponent.rubricDetailsSelected(questionId, rubricItems);
    } else if ($expandedDisplay.length === 0) {
        if (responseTracker !== undefined) {
            $targetElement.after(
                `<div class="apella-responses ${questionType}" questionId="${questionId}"></div>`
            )
            responseTracker.renderDetailedDisplay();
        } else {
            console.error(`Error finding response tracker for question id "${questionId}"`)
            // TODO: have this logged to the server
        }
    } else {
        $expandedDisplay.toggle();
    }
}

let vueComponent = undefined;
export default {
    initialize(studentList, component) {
        $('body').on('click', '.apella-question', toggleDetailedResponseDisplay);
        for (const student of studentList) {
            studentMap[student.id] = student;
        }

        vueComponent = component;
    },
    initializeDisplays(response_map) {
        for (const [questionId, responseList] of Object.entries(response_map)) {
            const $questionElement = $(`.apella-question[questionId="${questionId}"]`);
            const questionType = $questionElement.attr('type');
            let tracker;
            if (questionType === 'choice') {
                tracker = new ChoiceResponseDataView(responseList, questionId, $questionElement);
                tracker.renderSummary();
            } else if (questionType === 'paragraph') {
                tracker = new ParagraphResponseDataView(responseList, questionId);
            } else if (questionType === 'inline-text') {
                tracker = new InlineTextResponseDataView(responseList, questionId);
            } else if (questionType === 'inline-select') {
                tracker = new InlineSelectResponseDataView(responseList, questionId, JSON.parse($questionElement.attr('options')));
            } else if (questionType === 'rubric') {
                tracker = new RubricResponseDataView(responseList, questionId);
            }
            if (tracker !== undefined) {
                questionResponseTrackers[questionId] = tracker;
            }
        }
    },
    updateResponse(questionId, response) {
        questionResponseTrackers[questionId].updateResponse(response);
    }
}
