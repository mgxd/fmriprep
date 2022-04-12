"""TODO: Port to Niworkflows / Nipype"""
from nipype.interfaces.base import (
    CommandLine,
    CommandLineInputSpec,
    File,
    TraitedSpec,
    traits,
)


class _MSMInputSpec(CommandLineInputSpec):
    in_mesh = File(
        argstr="--inmesh %s",
        exists=True,
        desc="Input mesh (available formats: VTK, ASCII, GIFTI). Needs to be a sphere",
    )
    out_file = File(argstr="--out %s", desc="Output basename")
    reference_mesh = File(
        argstr="--refmesh %s",
        desc="Reference mesh (available formats: VTK, ASCII, GIFTI). Needs to be a sphere. "
        "If not included algorithm assumes reference mesh is equivalent input",
    )
    in_data = File(
        argstr="--indata %s",
        desc="Scalar or multivariate data for input - can be ASCII (.asc,.dpv,.txt) or "
        "GIFTI (.func.gii or .shape.gii)",
    )
    reference_data = File(
        argstr="--refdata %s",
        desc="Scalar or multivariate data for reference - can be ASCII (.asc,.dpv,.txt) or "
        "GIFTI (.func.gii or .shape.gii)",
    )
    transformed_mesh = File(
        argstr="--trans %s",
        desc="Transformed source mesh (output of a previous registration). Use this to "
        "initiliase the current registration.",
    )
    in_register = File(
        argstr="--in_register %s",
        desc="Input mesh at data resolution. Used to resample data onto input mesh if data is "
        "supplied at a different resolution. Note this mesh HAS to be in alignment with either "
        "the input_mesh of (if supplied) the transformed source mesh. Use with supreme caution.",
    )
    in_weight = File(
        argstr="--inweight %s",
        desc="Cost function weighting for input - weights data in these vertices when "
        "calculating similarity (ASCII or GIFTI). Can be multivariate provided dimension "
        "equals that of data ",
    )
    reference_weight = File(
        argstr="--refweight %s",
        desc="Cost function weighting for reference - weights data in these vertices when "
        "calculating similarity (ASCII or GIFTI). Can be multivariate provided dimension equals "
        "that of data",
    )
    config_file = File(argstr="--conf %s", desc="Configuration file")
    levels = traits.Int(
        argstr="--levels %d",
        desc="Number of resolution levels (default = number of resolution levels specified by "
        "--opt in config file)",
    )
    smooth_sigma = traits.Float(
        argstr="--smoothout %f", desc="Smooth tranformed output with this sigma (default=0)"
    )
    verbose = traits.Bool(argstr="--verbose", desc="Display diagnostic messages")


class _MSMOutputSpec(TraitedSpec):
    out_file = File(desc="Output file")


class MSM(CommandLine):
    """
    MSM (Multimodal Surface Matching) is a spherical registration tool which learns a mapping
    between multimodal (or multivariate/multichannel) cortical feature maps from two brains.

    Examples of the types of data which you can use can include:
    - morphological (sulcal depth or curvature) maps
    - cortical myelination
    - task or rest fMRI
    - tract density maps

    References
    ----------

    Robinson, Emma C., Saad Jbabdi, Matthew F. Glasser, Jesper Andersson, Gregory C. Burgess,
    Michael P. Harms, Stephen M. Smith, David C. Van Essen, and Mark Jenkinson. "MSM: A new
    flexible framework for Multimodal Surface Matching." Neuroimage 100 (2014): 414-426.

    Robinson, E.C., Garcia, K., Glasser, M.F., Chen, Z., Coalson, T.S., Makropoulos, A.,
    Bozek, J., Wright, R., Schuh, A., Webster, M. and Hutter, J., 2017. Multimodal surface
    matching with higher-order smoothness constraints. NeuroImage.

    Ishikawa, Hiroshi. "Higher-order clique reduction without auxiliary variables." Proceedings
    of the IEEE Conference on Computer Vision and Pattern Recognition. 2014.

    N. Komodakis and G. Tziritas "Approximate Labeling via Graph-Cuts Based on Linear
    Programming". IEEE Transactions on Pattern Analysis and Machine Intelligence, 2007.

    Glocker, Ben, et al. "Triangleflow: Optical flow with triangulation-based higher-order
    likelihoods." European Conference on Computer Vision. Springer Berlin Heidelberg, 2010.
    """
    _cmd = "msm"
    input_spec = _MSMInputSpec
    output_spec = _MSMOutputSpec

    def _list_outputs(self):
        outputs = self._outputs().get()
        return outputs['out_file']
