library(drc)

get_sigmoid_fitting_result = function(df_data, top="", bottom="", ec50=""){
    # if no constraint than top, bottom, ec50 = ""
    # if fixed_value constraint, top = list(fix=fix_value)
    # if min/max constraints, top = list(max=max_value, min=min_value)
    # for ec50 only 'fix' constraint works
    
    # if (top=="") {
    if (length(top) < 1) {
        top = list(fix=NA)
    }
    # if (bottom=="") {
    if (length(bottom) < 1) {
        bottom = list(fix=NA)
    }
    # if (ec50=="") {
    if (length(ec50) < 1) {
        ec50 = list(fix=NA)
    }
    if (! ("fix" %in% names(top))){
        top$fix = NA
    }
    if (! ("fix" %in% names(bottom))){
        bottom$fix = NA
    }
    if (! ("fix" %in% names(ec50))){
        ec50$fix = NA
    }
    result_list <- list()
    compound_name_vector = names(df_data)[2:length(df_data)]  # get compound names vector except first 'dose' column
    for (curr_name in compound_name_vector){
        df_curr <- df_data[!is.na(df_data[, curr_name]),c("dose", curr_name)]
        curr_measurement = df_curr[, curr_name]
        curr_dose = df_curr[, "dose"]
        curr_result = list()
        fixed_bottom = bottom$fix
        fixed_top = top$fix
        fixed_ec50 = ec50$fix
        try({
#             if (top=="" & bottom==""){
#                 curr_model = drm(curr_measurement ~ dose, data=df_curr, fct=LL.4(names=c("Hill slope", "Min", "Max", "EC50")))
#             } else if (top=="" & bottom!=""){
#                 curr_model = drm(curr_measurement ~ dose, data=df_curr, fct=LL.4(fixed=c(NA, fixed_bottom, NA, NA), names=c("Hill slope", "Min", "Max", "EC50")))
#             } else if (top!="" & bottom==""){
#                 curr_model = drm(curr_measurement ~ dose, data=df_curr, fct=LL.4(fixed=c(NA, NA, fixed_top, NA), names=c("Hill slope", "Min", "Max", "EC50")))
#             } else if (top!="" & bottom!=""){
#                 curr_model = drm(curr_measurement ~ dose, data=df_curr, fct=LL.4(fixed=c(NA, fixed_bottom, fixed_top, NA), names=c("Hill slope", "Min", "Max", "EC50")))
#             }
            refit = TRUE
            while(refit){
                curr_model = drm(curr_measurement ~ dose, data=df_curr, fct=LL.4(fixed=c(NA, fixed_bottom, fixed_top, fixed_ec50), names=c("Hill slope", "Min", "Max", "EC50")))
                curr_result <- summary(curr_model)
                item_position = 2
                if (is.na(fixed_bottom)){
                    fitted_bottom = curr_result[['coefficients']][item_position]
                    item_position = item_position + 1
                } else {
                    fitted_bottom = fixed_bottom
                }
                if (is.na(fixed_top)){
                    fitted_top = curr_result[['coefficients']][item_position]
                } else {
                    fitted_top = fixed_top
                }
#                 fitted_bottom = curr_result[2][1]
#                 fitted_top = curr_result[2][2]
                refit = FALSE
                #print(top)
                #print("max" %in% names(top))
                #print((("max" %in% names(top)) & (fitted_top > top$max)))
                if ("max" %in% names(top)){
                    if (fitted_top > top$max){
                        refit = TRUE
                        fixed_top = top$max
                    }
                }
                if ("min" %in% names(top)){
                    if (fitted_top < top$min){
                        refit = TRUE
                        fixed_top = top$min
                    }
                }
                if ("max" %in% names(bottom)){
                    if (fitted_bottom > bottom$max){
                        refit = TRUE
                        fixed_bottom = bottom$max
                    }
                }
                if ("min" %in% names(bottom)){
                    if (fitted_bottom < bottom$min){
                        refit = TRUE
                        fixed_bottom = bottom$min
                    }
                }
            }

            #curr_result <- summary(curr_model)
            #print(curr_result)
            # r^2 calc
            pred_error = PR(curr_model, curr_dose) - curr_measurement
            ss_res = sum(pred_error^2)
            ss_tot = sum((curr_measurement - mean(curr_measurement))^2)
            curr_result$r2 = 1 - ss_res / ss_tot
            if (is.na(fixed_bottom)){
                curr_result$bottom_fix = ""
            } else {
                curr_result$bottom_fix = fixed_bottom
            }
            if (is.na(fixed_top)){
                curr_result$top_fix = ""
            } else {
                curr_result$top_fix = fixed_top
            }
            if (is.na(fixed_ec50)){
                curr_result$ec50_fix = ""
            } else {
                curr_result$ec50_fix = fixed_ec50
            }
        })
        #print(c("===========", curr_name))
        #print(c("===========", curr_name, curr_result$r2))
        #print(curr_result)

        # append current result to output object
        result_list[[curr_name]] = curr_result
    }
    return(result_list)
}
