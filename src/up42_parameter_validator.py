import collections
import logging

from src.parameter_requirements import BLOCKS_PARAMETER_REQUIREMENTS


class UP42ParamaterValidator:
    def __init__(self, input_parameters):
        self.input_parameters = input_parameters

    def check_data_block(self, block_input_param_name, error_dict, all_input_param):
        """
        Compares the required parameters from BLOCKS_PARAMETER_REQUIREMENTS
        dict to data block. Because the data block name may vary but the
        parameters stay the same (ex. limit), we data block names have not
        been hardcoded and are treated differently.
        """
        for parameter, value in BLOCKS_PARAMETER_REQUIREMENTS[
            block_input_param_name
        ]["data_block"].items():
            if parameter == "limit":
                breakpoint()
                data_block = list(all_input_param.keys())[0]
                try:
                    assert (
                        all_input_param[data_block][parameter] >= value
                    )

                except AssertionError:
                    error_dict[block_input_param_name].append(
                        f"The {parameter} parameter in "
                        f"{block_input_param_name} should be {value} or more"
                    )
            else:
                breakpoint()
                data_block = list(all_input_param.keys())[0]
                try:
                    assert (
                        all_input_param[data_block][parameter] == value
                    )

                except ValueError:
                    error_dict[block_input_param_name].append(
                        f"The {parameter} parameter in "
                        f"{block_input_param_name} should be {value}"
                    )

        return error_dict

    # TODO this does not catch the edge case when
    # the same processing block is used twice
    def check_processing_blocks(
        self, block_input_param_name, block_with_requirements, error_dict, all_input_param
    ):
        """
        Compares the required parameters from BLOCKS_PARAMETER_REQUIREMENTS
        dict to processing blocks in the workflow chain.
        """
        for parameter, value in BLOCKS_PARAMETER_REQUIREMENTS[block_input_param_name][block_with_requirements].items():

            try:
                assert (all_input_param[block_with_requirements][parameter]== value)
            except AssertionError:
                error_dict[block_input_param_name].append(
                    f"The {parameter} parameter in "
                    f"{block_input_param_name} should be {value}"
                )

        return error_dict

    def handle_blocks_with_requirements(
        self, block_input_param_name, error_dict, all_input_param
    ):
        """
        Checks parameters of each block in the workflow chain based on
        requirements specified in the BLOCKS_PARAMETER_REQUIREMENTS dict.
        """
        logging.info(
            f"The {block_input_param_name} block has special requirements"
        )
        for block_with_requirements in BLOCKS_PARAMETER_REQUIREMENTS[block_input_param_name].keys():
            if block_with_requirements == "data_block":
                error_dict = self.check_data_block(
                    block_input_param_name=block_input_param_name,
                    error_dict=error_dict,
                    all_input_param=all_input_param
                )
            elif block_with_requirements in all_input_param.keys():
                error_dict = self.check_processing_blocks(
                    block_input_param_name=block_input_param_name,
                    block_with_requirements=block_with_requirements,
                    error_dict=error_dict,
                    all_input_param=all_input_param
                )

        return error_dict

    def check_parameters(self):
        """
        Check if input params match the params that are defined in the "
        "BLOCKS_PARAMETER_REQUIREMENTS dict.
        """
        # iterate through blocks from input parameters
        error_dict = collections.defaultdict(list)
        all_input_param = {}
        input_param_dict = self.input_parameters.dict()
        # filtered = {k: v for k, v in input_param_dict.items() if v is not None}
        for key, val in input_param_dict.items(): # TODO make dict comprehension
            if key.endswith(":1"):
                all_input_param[key] = val
            elif val is not None: # TODO make dict comprehension
                new_key = key + ":1"
                all_input_param[new_key] = val
        #
        # filtered = {key:val for key, val in input_param_dict.items() if key.endswith(":1")}
        # input_param_dict.clear()
        # input_param_dict.update(filtered)
        for block_in_input_param in all_input_param.keys():
            # blocks in input parameters are stored ad "block_name:1"
            if block_in_input_param in BLOCKS_PARAMETER_REQUIREMENTS.keys():
                error_dict = self.handle_blocks_with_requirements(
                    block_input_param_name=block_in_input_param,
                    error_dict=error_dict,
                    all_input_param=all_input_param
                )

            else:
                pass


        return error_dict
