"use strict";

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var CustomTableOptionChain = function (_BlinkElement) {
    _inherits(CustomTableOptionChain, _BlinkElement);

    function CustomTableOptionChain(args) {
        _classCallCheck(this, CustomTableOptionChain);

        var _this = _possibleConstructorReturn(this, _BlinkElement.call(this));

        var attr = B.extractArgAttrs(args);
        _this.state = new B.State({
            colData: attr.colData || [],
            rowData: attr.rowData || [],
            allData: attr.rowData || [],
            totalRowFieldId: attr.totalRowFieldId,
            expriyFilterFieldId: attr.expriyFilterFieldId,
            strikeFilterFieldId: attr.strikeFilterFieldId,
            ltp: attr.ltp || 0,
            symbol: attr.symbol || "",
            type: attr.type,
            loading: true
        });

        var self = _this;
        if (Object.keys(_this.state.rowData).length === 0) {
            _this.state.rowData = [];
            _this.state.allData = [];
        }

        _this.filterData = function (data, condition) {
            var total = {
                CE: {
                    totOI: 0,
                    totVol: 0
                },
                PE: {
                    totOI: 0,
                    totVol: 0
                }
            };

            var filteredData = data.filter(function (e) {
                if (condition(e)) {
                    if (e.CE) {
                        total.CE.totOI += e.CE.openInterest;
                        total.CE.totVol += e.CE.totalTradedVolume;
                    }
                    if (e.PE) {
                        total.PE.totOI += e.PE.openInterest;
                        total.PE.totVol += e.PE.totalTradedVolume;
                    }
                    return true;
                }
                return false;
            });

            return { filteredData: filteredData, total: total };
        };

        _this.updateBySP = function (allData, val, type) {
            var totalRowFieldId = _this.state.totalRowFieldId;
            var expriyFilterFieldId = _this.state.expriyFilterFieldId;
            var strikeFilterFieldId = _this.state.strikeFilterFieldId;

            var _this$filterData = _this.filterData(_this.state.allData, function (e) {
                var sp = [gsecType, currencyType].includes(type) ? CurrDecimalFixed(e.strikePrice) : DecimalFixed(e.strikePrice);
                return sp === val;
            }),
                filteredData = _this$filterData.filteredData,
                total = _this$filterData.total;

            filteredData = filteredData.sort(function (a, b) {
                return new Date(a.expiryDate) - new Date(b.expiryDate);
            });
            optionsState[type].filteredData = filteredData;
            optionsState[type].total = total;
            optionsState[type].type = "sp";
            optionsState[type].currType = type;

            B.get('/json/option-chain/option-chain_date.json').then(function (resp) {
                var respJSONObj = JSON.parse(resp);
                if (type === gsecType) {
                    respJSONObj.columns = respJSONObj.columns.filter(function (e) {
                        return e.heading !== 'IV';
                    });
                }
                if (type === "goldm") {
                    respJSONObj.columns = respJSONObj.columns.filter(function (e) {
                        return e.name !== 'chart';
                    });
                }
                switch (type) {
                    case "currency":
                        optionChain.state.colData = respJSONObj.columns;
                        optionChain.state.rowData = filteredData;
                        break;
                    default:
                        optionChain.state.colData = respJSONObj.columns;
                        optionChain.state.rowData = filteredData;
                }
                /*$(strikeFilterFieldId).show();
                $(expriyFilterFieldId).hide();
                $('#filterDivider').hide();
                $('#filterCurrDivider').hide();
                $('#filterGsecDivider').hide();
                $('#filterGoldMDivider').hide();*/
                $(expriyFilterFieldId + " select option[value=\"\"]").prop("selected", "selected");
                $(strikeFilterFieldId + " select option[value=\"" + val + "\"]").prop("selected", "selected");
                $("#" + totalRowFieldId + "-CE-totOI").text(DecimalFixed(total.CE.totOI));
                $("#" + totalRowFieldId + "-CE-totVol").text(DecimalFixed(total.CE.totVol));
                $("#" + totalRowFieldId + "-PE-totOI").text(DecimalFixed(total.PE.totOI));
                $("#" + totalRowFieldId + "-PE-totVol").text(DecimalFixed(total.PE.totVol));
                self.state.loading = false;
            });
        };

        _this.updateByDate = function (allData, val, type) {
            var totalRowFieldId = _this.state.totalRowFieldId;
            var expriyFilterFieldId = _this.state.expriyFilterFieldId;
            var strikeFilterFieldId = _this.state.strikeFilterFieldId;

            var _this$filterData2 = _this.filterData(allData, function (e) {
                return new Date(e.expiryDate).getTime() === new Date(val).getTime();
            }),
                filteredData = _this$filterData2.filteredData,
                total = _this$filterData2.total;

            optionsState[type].filteredData = filteredData;
            optionsState[type].total = total;
            optionsState[type].type = "date";
            optionsState[type].currType = type;

            B.get('/json/option-chain/option-chain.json').then(function (resp) {
                var respJSONObj = JSON.parse(resp);
                if (type === gsecType) {
                    respJSONObj.columns = respJSONObj.columns.filter(function (e) {
                        return e.heading !== 'IV';
                    });
                }

                if (type === "goldm") {
                    respJSONObj.columns = respJSONObj.columns.filter(function (e) {
                        return e.name !== 'chart';
                    });
                }

                switch (type) {
                    case "currency":
                        optionChain.state.colData = respJSONObj.columns;
                        optionChain.state.rowData = filteredData;
                        break;
                    default:
                        optionChain.state.colData = respJSONObj.columns;
                        optionChain.state.rowData = filteredData;
                }
                /*$(strikeFilterFieldId).hide();
                $(expriyFilterFieldId).show();
                $('#filterDivider').hide();
                $('#filterCurrDivider').hide();
                $('#filterGsecDivider').hide();*/
                $(strikeFilterFieldId + " select option[value=\"\"]").prop("selected", "selected");
                $(expriyFilterFieldId + " select option[value=\"" + val + "\"]").prop("selected", "selected");
                $("#" + totalRowFieldId + "-CE-totOI").text(DecimalFixed(total.CE.totOI));
                $("#" + totalRowFieldId + "-CE-totVol").text(DecimalFixed(total.CE.totVol));
                $("#" + totalRowFieldId + "-PE-totOI").text(DecimalFixed(total.PE.totOI));
                $("#" + totalRowFieldId + "-PE-totVol").text(DecimalFixed(total.PE.totVol));
                self.state.loading = false;
            });
        };

        var dom = table(_extends({}, attr.tableStyle), thead(tr({}, th({ "class": "text-center", "colspan": Math.floor(_this.state.colData.length / 2) }, "CALLS"), th({}, ""), th({ "class": "text-center", "colspan": Math.floor(_this.state.colData.length / 2) }, "PUTS")), tr({
            onStateChange: {
                state: _this.state, obj: 'colData', onChange: function onChange(e, v) {
                    e.empty();
                    var tableHeader = _this.state.colData.map(function (col, index) {
                        return th({ width: col.width, title: col.legend }, col.heading || '', span({}, ' ' + col.subHead));
                    });
                    B.renderAll(tableHeader, e);
                }
            }
        })), tbody({
            onStateChange: {
                state: _this.state, obj: 'rowData', onChange: function onChange(e, v) {
                    e.empty();
                    var rows = [];
                    if (_this.state.rowData.length > 0) {
                        _this.state.rowData.map(function (row, t) {
                            var rowDomObj = tr(concatArr([{}], _this.state.colData.map(function (col, index) {
                                var cellVal = col.optionType !== "" ? col.optionType === "CE" ? typeof row.CE === "undefined" ? null : row.CE[col.name] : typeof row.PE === "undefined" ? null : row.PE[col.name] : row[col.name];
                                var rowVal = col.optionType !== "" ? col.optionType === "CE" ? typeof row.CE === "undefined" ? null : row.CE : typeof row.PE === "undefined" ? null : row.PE : row;
                                var bgColor = col.optionType === "CE" && _this.state.ltp >= row["strikePrice"] ? "addCEBg" : "";
                                var bgColor_1 = col.optionType === "PE" && _this.state.ltp < row["strikePrice"] ? "addPEBg" : "";
                                var chkClass = bgColor === "addCEBg" || bgColor_1 === "addPEBg" ? 'bg-yellow' : '';
                                if (col.name !== "chart" && cellVal === undefined || cellVal === null) {
                                    var tdClass = chkClass + " text-center";
                                    return td({ width: col.width, class: tdClass }, "-");
                                }
                                var fcellVal = void 0;
                                if (col.type) {
                                    if (col.type === "number") {
                                        if ([gsecType, currencyType].includes(_this.state.type) && (col.heading && col.heading.toLowerCase().indexOf('price') >= 0 || col.legend && col.legend.toLowerCase().indexOf('price') >= 0)) {
                                            fcellVal = CurrDecimalFixed(cellVal).toString();
                                        } else {
                                            fcellVal = DecimalFixed(cellVal).toString();
                                        }
                                    }
                                    if (col.type === "quantity") {
                                        fcellVal = DecimalFixed(cellVal, true).toString();
                                    }
                                } else {
                                    fcellVal = cellVal ? cellVal.toString() : '-';
                                }
                                if (col.chkVal) {
                                    var chkValClass = "";
                                    if (cellVal < 0) {
                                        chkValClass += 'redTxt';
                                    } else if (cellVal > 0) {
                                        chkValClass += 'greenTxt';
                                    }
                                    var _tdClass = chkClass + " " + chkValClass;
                                    return td({
                                        width: col.width,
                                        class: _tdClass
                                    }, fcellVal);
                                } else if (col.name === "chart") {
                                    var ceIdentifier = row.CE && row.CE["identifier"];
                                    var peIdentifier = row.PE && row.PE["identifier"];
                                    var ocSP = row.strikePrice;
                                    var ocED = row.expiryDate;
                                    var ocUnderlying = row.CE && row.CE["underlying"] || row.PE && row.PE["underlying"];
                                    return td({ width: col.width }, a({ "href": "javascript:;", 'onclick': 'genChainGraph(\'' + ceIdentifier + '\',\'' + peIdentifier + '\', \'' + ocSP + '\', \'' + ocED + '\', \'' + ocUnderlying + '\')', 'data-toggle': 'modal', 'data-target': '#modal_oc_graph' }, img({
                                        "src": "/assets/images/grficon.gif",
                                        "alt": "Graph"
                                    }, '')));
                                } else if (col.name === "strikePrice") {
                                    return td({
                                        width: col.width,
                                        on: {
                                            'click': function click(e) {
                                                _this.updateBySP(_this.state.allData, fcellVal, _this.state.type);
                                            }
                                        }
                                    }, a({ "class": "bold", "href": "javascript:;" }, fcellVal));
                                } else if (col.name === "expiryDate") {
                                    return td({
                                        width: col.width,
                                        on: {
                                            'click': function click(e) {
                                                _this.updateByDate(_this.state.allData, fcellVal, _this.state.type);
                                            }
                                        }
                                    }, a({ "href": "javascript:;" }, fcellVal));
                                } else if (col.heading === 'LTP') {
                                    var url = void 0;
                                    switch (_this.state.type) {
                                        case currencyType:
                                            url = "/currency-getquote?identifier=" + rowVal.identifier;
                                            break;
                                        case gsecType:
                                            url = "/interest-rate-future-getquote?symbol=" + rowVal.underlying + "&identifier=" + rowVal.identifier;
                                            break;
                                        case goldmType:
                                            url = "/commodity-getquote?symbol=" + rowVal.underlying + "&identifier=" + rowVal.identifier;
                                            break;
                                        default:
                                            url = "/get-quotes/derivatives?symbol=" + rowVal.underlying + "&identifier=" + rowVal.identifier;

                                    }

                                    return td({ width: col.width, class: chkClass }, a({ "class": "bold", "href": url, "target": "_blank" }, fcellVal));
                                } else {
                                    return td({
                                        width: col.width,
                                        class: chkClass
                                    }, fcellVal);
                                }
                            })));

                            rows.push(rowDomObj);
                        });
                    } else {
                        rows.push(tr(td({ colspan: _this.state.colData.length, class: 'text-center emptyRow' }, "No Record Found")));
                    }
                    B.renderAll(rows, e);
                }
            }
        }));
        //mandatory code for a BlinkUI component
        _this.args = dom.args;
        _this.elem = dom.elem;
        _this.elem.cmp = _this;
        //mandatory code for a BlinkUI component ends
        return _this;
    }

    return CustomTableOptionChain;
}(BlinkElement);

instantiate('CustomTableOptionChain', CustomTableOptionChain);